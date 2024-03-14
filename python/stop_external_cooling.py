#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from https://github.com/JJandke
#
# "1" stands for "off" and "0" stands for "on", because the relay module I use does not switch when the current is present, but at 0V it does.
# However, I only want current to flow at the relay, when the fan is running.
# Therefore, another wiring is not possible and the problem must be solved on software side.
# With other relay modules it might be that "0" and "1" have to be exchanged. Of course, 0 and 1 can also be replaced by "True" and "False" or "GPIO.HIGH" and "GPIO.LOW".

import datetime
import RPi.GPIO as GPIO
import logging
import pigpio
import os


try:
    logging.basicConfig(filename="/home/config/log/external_cooling.log", level=logging.DEBUG)
    now = datetime.datetime.now()
    log_time = now.strftime("%a-%d.%m.%Y-%H:%M:%S ")

except Exception as e:
    print(e)
    print("FATAL ERROR! - Could not set up logging, exiting!")
    sys.exit(-1)


# Create log file if it does not exist.
try:
    if not os.path.isfile("/home/config/log/external_cooling.log"):
        logging.debug("{0}Logfile does not exist, therefore we will create it...".format(log_time))
        f = open("/home/config/log/external_cooling.log", "x")
        f.close()
        logging.debug("{0}sucessfully created logfile".format(log_time))
        
    else:
        logging.debug("{0}Logfile already exists".format(log_time))
        pass

except Exception as e:
    logging.error("{0}".format(log_time), e)
    logging.error("{0}Could not setup logfile, exiting!".format(log_time))
    print("FATAL ERROR! - Could not set up logfile, exiting!")
    sys.exit(-1)


try:
    logging.debug("{0}Trying to set up GPIOs".format(log_time))

    GPIO.setmode(GPIO.BCM)
    logging.debug("{0}GPIO mode has been set to BCM".format(log_time))
    
    GPIO.setwarnings(False)     # set setwarnings = False if another script uses the GPIO
    logging.debug("{0}GPIO-Warnings have been deactivated".format(log_time))

    GPIO.setup(17, GPIO.OUT)    # HDD Relay
    logging.debug("{0}GPIO #17 has been set as OUT".format(log_time))

    GPIO.setup(23, GPIO.OUT)    # HDD PWM
    logging.debug("{0}GPIO #23 has been set as OUT".format(log_time))

    pwm = pigpio.pi()
    logging.debug("{0}pigpio.pi() is now pwm".format(log_time))
    logging.debug("{0}GPIO successfully configured".format(log_time))

except Exception as e:
    logging.error("{0}".format(log_time), e)
    logging.error("{0}Could not setup GPIOs, exiting!".format(log_time))
    sys.exit(-1)


# It checks if the files exist. If they do, they will be deleted. If they do not exist, fade.py or strobe.py will stop if they are running.
try:
    if os.path.exists("/home/config/code/python/.kill_cooling.txt"):
        logging.debug("{0}Killswitch is existing. We will delete it...".format(log_time))
        os.remove("/home/config/code/python/.kill_cooling.txt")
        logging.debug("{0}Killswitch sucessfully deleted".format(log_time))


    GPIO.output(17, 1)
    pwm.set_PWM_dutycycle(23, 0)
    logging.info("{0}Stopped external cooling".format(log_time))

except Exception as e:
    logging.debug("{0}Could not stop external cooling: {1}".format(log_time, e))
