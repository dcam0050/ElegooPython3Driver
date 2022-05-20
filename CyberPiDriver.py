# -*- coding: utf-8 -*-
# Copyright (c) 2018, Cyberselves
# Author: Daniel Camilleri

import logging
from time import sleep
import numpy as np
import cv2
import animus_utils as utils
import math
import os
from picamera.array import PiRGBArray
from picamera import PiCamera
import pantilthat
import websocket
import os
from enum import Enum

defaultIP = "192.168.1.227"


class CyberPiDriver:
    def __init__(self, robot_model, robot_name):

        self.log = utils.create_logger(robot_name + "-Direct", logging.INFO)
        self.robot_name = robot_name

        # VISION PARAMETERS
        self.hres = 320
        self.vres = 240
        self.captureObject = None
        self.rawCapture = None
        self.mainCamera = utils.PyImageSample(
            source="main",
            image_type=utils.ImageSample.RGB,
            compression=utils.ImageSample.RAW,
            transform=utils.Transform()
        )

        # AUDITION PARAMETERS
        self.audio_params = utils.AudioParams(
            Backends=["pulseaudio"],
            SampleRate=32000,
            Channels=1,
            SizeInFrames=True,
            TransmitRate=20
        )

        ESP_IP = os.getenv('ESP_IP')
        if ESP_IP == "":
            logging.info("ESP IP not provided. Using default - {}".format(defaultIP))
            ESP_IP = defaultIP

        self.esp_url = "http://{}/ws".format(ESP_IP)
        logging.info("Sending test command to {}".format(self.esp_url))

        self.esp_websocket_client = websocket.WebSocket()
        self.esp_websocket_client.connect(self.esp_url)
        self.esp_websocket_client.send("5")

    def get_audio_parameters(self):
        return self.audio_params

    # ----------------------------------VISION--------------------------------
    def vision_initialise(self):
        # Success return True
        # Failure return False
        try:
            self.vid_capture = cv2.VideoCapture()
            self.vid_capture.open(0)
            test_img = self.vid_capture.read()

            if len(test_img[1].shape) == 3:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def vision_get(self):
         # Success return 3 dimensional numpy array
        # Failure return None
        result, image = self.vid_capture.read()

        if result:
            # image = cv2.resize(image, (120, 160))
            # image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # image = cv2.flip(image, 1)
            image_frame = utils.PyImageSample(
                source="RightCamera",
                image_type=utils.ImageSample.RGB,
                compression=utils.ImageSample.RAW,
                transform=utils.Transform()
            )
            img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image_frame.encode_image(img)
            return image_frame
        else:
            return None

    def vision_close(self):
        # No return
        self.vid_capture.release()

    # ----------------------------------AUDITION--------------------------------

    def audition_initialise(self):
        # mode defines structure for audio return
        # Success return True
        # Failure return False
        return True

    def audition_get(self):
        # Success return numpy array
        # Failure return None
        return None

    def audition_close(self):
        # No return
        pass

    # ----------------------------------PROPRIOCEPTION--------------------------------

    def proprioception_initialise(self):
        # Success return True
        # Failure return False
        return True
    
    def proprioception_get(self):
        # joints defines subset of joints to return for robot
        # Success return numpy vector (array with 1 dimension or singleton 2nd dimension)
        # Failure return None
        return [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    
    def proprioception_close(self):
        # No return
        pass

    # ----------------------------------MOTOR--------------------------------
    def motor_initialise(self):
        # Take into consideration self.use_effectors and self.move_around when initialising motors
        # Success return True
        # Failure return False
        pantilthat.pan(0)
        pantilthat.tilt(0)
        return True

    def motor_set(self, motor_sample):
        loco = [motor_sample.Locomotion.Position.x,
                motor_sample.Locomotion.Position.y,
                motor_sample.Locomotion.Rotation.z]

        return True

    def motor_close(self):
        # No return
        pass

    # ----------------------------------SPEECH--------------------------------
    def speech_initialise(self, language="English"):
        # Take into consideration language when initialising speech
        # Success return True
        # Failure return False
        return True
    
    def speech_set(self, sentence):
        # No return
        self.log.info("Elegoo Robot says: '" + sentence + "'")
    
    def speech_close(self):
        # No return
        pass

    # ----------------------------------AUDIO OUT--------------------------------
    def voice_initialise(self):
        # self.voice_keys = set(list(AudioSample._fields))
        # Take into consideration language when initialising speech
        # Success return True
        # Failure return False
        return True

    # TODO assert data types
    def voice_set(self, voices_data):
        pass

    def voice_close(self):
        # No return
        pass

    # ----------------------------------EMOTION--------------------------------
    def emotion_initialise(self):
        # Success return True
        # Failure return False
        return True

    def emotion_set(self, emotion_name):
        if emotion_name in utils.emotions_list:
            getattr(self, "set_"+emotion_name)()
        else:
            raise ValueError("emotion {} not in standardised emotions list: {}"
                             .format(emotion_name, utils.emotions_list))

    def set_angry(self):
        self.log.info("Feeling angry")

    def set_fear(self):
        self.log.info("Feeling fear")

    def set_sad(self):
        self.log.info("Feeling sad")

    def set_happy(self):
        self.log.info("Feeling happy")

    def set_surprised(self):
        self.log.info("Feeling surprised")

    def set_neutral(self):
        self.log.info("Feeling neutral")

    def emotion_close(self):
        # No return
        pass


class Movement(Enum):
    UP = "1"
    DOWN = "2"
    LEFT = "3"
    RIGHT = "4"
    UP_LEFT = "5"
    UP_RIGHT = "6"
    DOWN_LEFT = "7"
    DOWN_RIGHT = "8"
    TURN_LEFT = "9"
    TURN_RIGHT = "10"
    STOP = "0"
