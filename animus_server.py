#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2020, Cyberselves Universal Ltd.
# All Rights Reserved
# Author: Daniel Camilleri <daniel@cyberselves.com>

import argparse
import os
import sys
import json
import logging
from importlib import import_module
from functools import partial
import time
import animus_robot as animus
import animus_utils as utils

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time
import threading
import _thread

log = utils.create_logger("Server", logging.INFO)
robotDriver = None
stopServer = False


def raw_input_with_timeout(prompt, timeout=30.0):
    print(prompt,)
    timer = threading.Timer(timeout, _thread.interrupt_main)
    astring = None
    try:
        timer.start()
        astring = input(prompt)
    except KeyboardInterrupt:
        astring = "y"
    except SystemExit:
        astring = "y"
    except SystemError:
        astring = "y"
    timer.cancel()
    return astring


def make_georange(upper_lat, lower_lat, upper_long, lower_long):
    ret = dict()
    ret["UpperLat"] = upper_lat
    ret["LowerLat"] = lower_lat
    ret["UpperLong"] = upper_long
    ret["LowerLong"] = lower_long
    return ret


def get_robot_driver(robot_details, search_dir, dev_mode):
    module_name = robot_details.model + "Driver"
    driver_name = module_name + ".py"

    log.info("Looking for {}".format(driver_name))

    if dev_mode:
        for f in os.listdir(search_dir):
            if f == driver_name:
                robotImport = import_module(module_name, os.path.join(search_dir, driver_name))
                return getattr(robotImport, module_name)
    else:
        try:
            robotImport = import_module(module_name)
            return getattr(robotImport, module_name)
        except ImportError:
            return None

    return None


def get_robot_extensions(robot_details, search_dir):
    module_name = robot_details.model + "Extensions"
    driver_name = module_name + ".py"

    log.info("Looking for {}".format(driver_name))
    for f in os.listdir(search_dir):
            if f == driver_name:
                path = os.path.join(search_dir, driver_name)
                log.info("{} found at {}".format(driver_name, path))
                log.info("Opening module {}...".format(module_name))

                robotImport = import_module(module_name, os.path.join(search_dir, driver_name))
                return getattr(robotImport, module_name)

def action_handler(result, fps):
    global robotDriver
    success = getattr(robotDriver, result.modality+"_set")(result.data)


def output_modality_handler(modality_name, result, fps):
    return animus.set_modality(modality_name, result)


def main():
    global robotDriver
    global stopServer

    parser = argparse.ArgumentParser()
    parser.add_argument('--devMode', default=False, help='Import driver in development mode')
    args = parser.parse_args()
    devmode = args.devMode

    log.info("Starting server")
    log.info("\n" + animus.version().decode())

    # Setup server
    setup_result = animus.setup("AnimusPython3Server")
    if not setup_result.success:
        log.error(setup_result.description)
        sys.exit(-1)

    read_robot_config_result = animus.read_robot_config()

    if not read_robot_config_result.error.success:
        log.error(read_robot_config_result.error.description)
        sys.exit(-1)

    robotDetails = read_robot_config_result.robot
    server_install_dir = os.path.dirname(os.path.realpath(sys.argv[0]))

    log.info("This is a {} robot made by {} called {}".format(robotDetails.model,
                                                              robotDetails.make,
                                                              robotDetails.name))

    # Check if there are any robot extensions present
    robotExtClass = get_robot_extensions(robotDetails, server_install_dir)

    robotDriverClass = get_robot_driver(robotDetails, server_install_dir, devmode)

    if robotDriverClass is None:
        log.error("Could not find robot driver. Aborting...")
        sys.exit(-1)

    if robotExtClass is not None:
        robotExt = robotExtClass(log)
    else:
        robotExt = None

    if robotExt is not None:
        robotExt.additional_setup()

    input_mods, output_mods = utils.discover_modalities(robotDriverClass)
    robotDetails.robot_config.input_modalities.extend(input_mods)
    robotDetails.robot_config.output_modalities.extend(output_mods)

    log.info("Input modalities: {} \n Output Modalities: {}".format(robotDetails.robot_config.input_modalities,
                                                                    robotDetails.robot_config.output_modalities))

    robotDriver = robotDriverClass(robotDetails.model, robotDetails.name)

    # Get audio details for robot
    robotDetails.robot_config.StrAudioParams.CopyFrom(robotDriver.get_audio_parameters())
    if "notinternal" in robotDetails.robot_config.StrAudioParams.Backends:
        while len(robotDetails.robot_config.internal_modalities) > 0:
            robotDetails.robot_config.internal_modalities.pop()

    # At this point we are ready to initialise robot comms
    start_comms_result = animus.start_robot_comms(robotDetails, True, True)
    if not start_comms_result.success:
        log.error(start_comms_result.description)
        sys.exit(-1)

    open_modalities = []

    # Start all modalities
    pool_count = 1
    for mod in input_mods+output_mods:
        success = getattr(robotDriver, mod + "_initialise")()
        if success:
            open_modalities.append(mod)

        if mod not in robotDetails.robot_config.internal_modalities and mod in output_mods:
            pool_count += 1

    executor = ThreadPoolExecutor(max_workers=pool_count)

    action_periodic_sampler = utils.PeriodicSampler("RobotAction", animus.get_next_action, 200, devmode, action_handler)
    future = executor.submit(action_periodic_sampler.run)

    # # Start output modality sampling
    output_mod_samplers = dict()
    for mod in output_mods:
        if mod in open_modalities and mod not in robotDetails.robot_config.internal_modalities:
            samp_func = getattr(robotDriver, mod + "_get")
            log.info("Creating output loop for {} modality".format(mod))
            output_mod_samplers[mod] = utils.PeriodicSampler(mod, samp_func, 40, devmode, partial(output_modality_handler, mod))
            executor.submit(output_mod_samplers[mod].run)

    if robotExt is not None:
        robotExt.setup_complete(open_modalities, robotDriver, robotDetails)
        if "speech" in open_modalities:
            robotDriver.speech_set("Powered by Cyberselves")
    else:
        if "speech" in open_modalities:
            robotDriver.speech_set("Cyberselves universal interface is up and running. My name is {} and I am ready to go.".format(robotDetails.name))

    if robotExt is not None:
        robotExt.wait_loop()
    else:
        print("Press y to exit")
        try:
            while True:
                pressed = raw_input_with_timeout("", 1)
                if pressed == "y":
                    log.info("Received exit event")
                    break
        except Exception as e:
            log.error(e)
        except KeyboardInterrupt:
            log.info("Closing down")
        except SystemExit:
            log.info("Closing down")

    if robotExt is not None:
        robotExt.additional_teardown()

    action_periodic_sampler.stop()
    for mod in output_mod_samplers:
        output_mod_samplers[mod].stop()

    for mod in open_modalities:
        log.info("Closing {} modality".format(mod))
        success = getattr(robotDriver, mod + "_close")()
        time.sleep(0.5)

    animus.close_robot_comms()


if __name__ == "__main__":
    main()
