# /usr/bin/python3
# -*- coding: utf-8 -*-
# from https://github.com/JJandke
#
# "1" stands for "off" and "0" stands for "on", because the relay module I use does not switch when the current is present, but at 0V it does.
# However, I only want current to flow at the relay, when the fan is running.
# Therefore, another wiring is not possible and the problem must be solved on software side.
# With other relay modules it might be that "0" and "1" have to be exchanged. Of course, 0 and 1 can also be replaced by "True" and "False" or "GPIO.HIGH" and "GPIO.LOW".

import RPi.GPIO as GPIO
import os
import sys
import time
import pigpio
import logging
import datetime

pwm = pigpio.pi()

# Create log file for this script
# Running the script will delete the old log file each time to save disk space and keep the file more organized.
if os.path.isfile("/home/config/log/external_cooling.log"):
    os.remove("/home/config/log/external_cooling.log")
    f = open("/home/config/log/external_cooling.log", "x")
    f.close()
else:
    f = open("/home/config/log/external_cooling.log", "x")
    f.close()

logging.basicConfig(filename="/home/config/log/external_cooling.log", level=logging.DEBUG)


day = datetime.datetime.now()
log_time = day.strftime("%a-%d.%m.%Y-%H:%M:%S ")
pwm_speed = 100


try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)     # set setwarnings = False if another script uses the GPIO
    GPIO.setup(17, GPIO.OUT)    # HDD Relay
    GPIO.setup(23, GPIO.OUT)    # HDD PWM
    logging.debug("{0}GPIO successfully configured".format(log_time))

except Exception as e:
    logging.error("{0}".format(log_time), e)

# activate fans
def cooling():
    if not os.path.exists("/home/config/code/python/.kill_cooling.tx"):
        os.mknod("/home/config/code/python/.kill_cooling.tx")                   # create killswitch file to show that cooling is active
    GPIO.output(17, 0)
    for pwm_speed in range(255):
        if os.path.exists("/home/config/code/python/.kill_cooling.txt"):        # checking if killswitch exists...
            pwm.set_PWM_dutycycle(23, pwm_speed)
            pwm_speed + 10
            time.sleep(10)
        else:
            GPIO.output(17, 0)                                                  # ...if not, stop cooling
            pwm.set_PWM_dutycycle(23, 0)
            sys.exit(0)

try:
    cooling()
    logging.debug("{0}started cooling".format(log_time))

except Exception as e:
    logging.error("{0}could not start cooling".format(log_time))
