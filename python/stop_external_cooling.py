#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from https://github.com/JJandke
#
# "1" stands for "off" and "0" stands for "on", because the relay module I use does not switch when the current is present, but at 0V it does.
# However, I only want current to flow at the relay, when the fan is running.
# Therefore, another wiring is not possible and the problem must be solved on software side.
# With other relay modules it might be that "0" and "1" have to be exchanged. Of course, 0 and 1 can also be replaced by "True" and "False" or "GPIO.HIGH" and "GPIO.LOW".

from datetime import datetime
import RPi.GPIO as GPIO
import logging
import pigpio
import os


logging.basicConfig(filename="/home/config/log/external_cooling.log", level=logging.DEBUG)
now = datetime.now()
pwm = pigpio.pi()
log_time = now.strftime("%a-%d.%m.%Y-%H:%M:%S ")



# Create log file if it does not exist.
if not os.path.isfile("/home/config/log/external_cooling.log"):
    logging.debug("logfile not existing... creating")
    f = open("/home/config/log/external_cooling.log", "x")
    f.close()
    logging.debug("logfile created")
else:
    logging.debug("logfile exists")
    pass


try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)     # set setwarnings = False if another script uses the GPIO
    GPIO.setup(17, GPIO.OUT)    # HDD Relay
    GPIO.setup(23, GPIO.OUT)    # HDD PWM
    logging.debug("{0}GPIO successfully configured".format(log_time))

except Exception as e:
    logging.error("{0}".format(log_time), e)


# It checks if the files exist. If they do, they will be deleted. If they do not exist, fade.py or strobe.py will stop if they are running.
try:
    if os.path.exists("/home/config/code/python/.kill_cooling.txt"):
        os.remove("/home/config/code/python/.kill_cooling.txt")

    GPIO.output(17, 1)
    pwm.set_PWM_dutycycle(23, 0)
    logging.info("{0}Stopped external cooling".format(log_time))

except Exception as e:
    logging.debug("{0}Could not stop external cooling: {1}".format(log_time, e))
