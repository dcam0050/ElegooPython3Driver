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

    def get_audio_parameters(self):
        return self.audio_params

    # ----------------------------------VISION--------------------------------
    def vision_initialise(self):
        self.camera = PiCamera()
        self.camera.resolution = (self.hres, self.vres)
        self.camera.framerate = 30
        self.rawCapture = PiRGBArray(self.camera, size=(self.hres, self.vres))
        self.captureObject = self.camera.capture_continuous(self.rawCapture, format="rgb", use_video_port=True)
        self.first = False
        return True

    def vision_get(self):
        frame = next(self.captureObject)
        if frame is None:
            return None

        image = cv2.flip(frame.array, -1)
        self.mainCamera.encode_image(image)
    
        # clear the stream in preparation for the next frame
        self.rawCapture.truncate(0)         
        return self.mainCamera

    def vision_close(self):
        self.camera.close()

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

    def motor_set(self, joint_angles_list):
        # p = joint_angles_list[0] + joint_angles_list[1]
        print(joint_angles_list)
        # pantilthat.pan(joint_angles_list[0])
        # pantilthat.tilt(joint_angles_list[1])
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
        self.log.info("ExampleRobot says: '" + sentence + "'")
    
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
