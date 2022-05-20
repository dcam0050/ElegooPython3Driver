# -*- coding: utf-8 -*-
# Copyright (c) 2020, Cyberselves Universal Ltd.
# All Rights Reserved
# Author: Daniel Camilleri <daniel@cyberselves.com>

from lib_robot import animus_robot_py3 as animus_robot
import animus_utils as utils
import logging
import json

log = utils.create_logger("AnimusRobot", logging.INFO)
_animus_robot_version = "v3.1.1"
_animus_robot_build = "1523"
_animus_core_version = "v3.0.2"
_sdk_version = "v2.0.20"
_sdk_build = "1951"
_sdk_build_date = "2022-05-03-20:31:17-UTC"


def version():
    return animus_robot.VersionGo()


def setup(logdir):
    setup_request = utils.SetupRobotProto(
        logDir=logdir,
        Debug=True,
    ).SerializeToString()

    return utils.Error().FromString(
        animus_robot.Setup(setup_request, len(setup_request))
    )


def read_robot_config():
    return utils.RobotConfigProto().FromString(
        animus_robot.ReadRobotConfig()
    )


def start_robot_comms(robot_details, start_local=True, start_remote=False):
    start_robot_request = utils.StartRobotCommsProto(
        startLocal=start_local,
        startRemote=start_remote,
        robot=robot_details
    ).SerializeToString()

    ret = utils.Error().FromString(
        animus_robot.StartRobotComms(start_robot_request, len(start_robot_request))
    )
    if ret.success:
        log.info("Robot communication interfaces started")
    else:
        log.error("Failed to open robot communication interfaces")

    return ret


def get_next_action(blocking=False):
    get_result = animus_robot.GetNextAction(int(blocking))
    sample = utils.ActionProto().FromString(get_result)

    if sample.error.success:
        new_sample = utils.RobotAction()
        new_sample.data = utils.decode_data(sample.sample)
        new_sample.modality = sample.modalityName
    else:
        new_sample = None
    return new_sample


def set_modality(modality_name, sample):
    dtype, data, data_len = utils.encode_data(sample)
    if dtype is not None:
        return utils.Error().FromString(
            animus_robot.SetModality(modality_name.encode(), dtype, data, data_len)
        )
    else:
        return False


def close_robot_comms():
    return utils.Error().FromString(
        animus_robot.CloseRobotComms()
    )

