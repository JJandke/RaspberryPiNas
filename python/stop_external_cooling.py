#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from https://github.com/JJandke
#

from datetime import datetime
import RPi.GPIO as GPIO
import logging
import pigpio
import os

now = datetime.now()
log_time = now.strftime("%a-%d.%m.%Y-%H:%M:%S ")
logging.basicConfig(filename="/home/config/log/external_cooling.log", level=logging.DEBUG)


# Create log file if it does not exist.
if not os.path.isfile("/home/config/log/external_cooling.log"):
    logging.debug("logfile not existing... creating")
    f = open("/home/config/log/external_cooling.log", "x")
    f.close()
    logging.debug("logfile created")
else:
    logging.debug("logfile exists")
    pass


logging.debug("start assigning variables")
pi = pigpio.pi()
logging.debug("assigned pi = pigpio.pi")







# It checks if the files exist. If they do, they will be deleted. If they do not exist, fade.py or strobe.py will stop if they are running.
try:
    if os.path.exists("/home/config/code/python/.kill_cooling.txt"):
        os.remove("/home/config/code/python/.kill_cooling.txt")

    pi.setGPIO.output(17, 0)
    pwm.set_PWM_dutycycle(23, 0)
    logging.info("{0}Stopped external cooling".format(log_time))

except Exception as e:
    logging.debug("{0}Could not stop external cooling: {1}".format(log_time, e))
