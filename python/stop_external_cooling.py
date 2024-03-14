#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from https://github.com/JJandke
#

from datetime import datetime
import RPi.GPIO as GPIO
import logging
import pigpio
import os

logging.basicConfig(filename="/home/config/log/external_cooling.log", level=logging.DEBUG)
logging.debug("start assigning variables")
pi = pigpio.pi()
logging.debug("assigned pi = pigpio.pi")
now = datetime.now()
log_time = now.strftime("%a-%d.%m.%Y-%H:%M:%S ")

# Create log file if it does not exist.
if not os.path.isfile("/home/config/log/external_cooling.log"):
    f = open("/home/config/log/external_cooling.log", "x")
    f.close()
else:
    pass



# It checks if the files exist. If they do, they will be deleted. If they do not exist, fade.py or strobe.py will stop if they are running.
try:
    if os.path.exists("/home/config/code/python/.kill_cooling.txt"):
        os.remove("/home/config/code/python/.kill_cooling.txt")

    pi.setGPIO.output(17, 0)
    pwm.set_PWM_dutycycle(23, 0)
    logging.info("{0}Stopped external cooling".format(log_time))

except Exception as e:
    logging.debug("{0}Could not stop external cooling: {1}".format(log_time, e))
