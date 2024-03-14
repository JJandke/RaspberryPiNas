#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from https://github.com/JJandke
#
# "1" stands for "off" and "0" stands for "on", because the relay module I use does not switch when the current is present, but at 0V it does.
# However, I only want current to flow at the relay, when the fan is running.
# Therefore, another wiring is not possible and the problem must be solved on software side.
# With other relay modules it might be that "0" and "1" have to be exchanged. Of course, 0 and 1 can also be replaced by "True" and "False" or "GPIO.HIGH" and "GPIO.LOW".


import os
import sys
import time
import pigpio
import logging
import datetime
import RPi.GPIO as GPIO


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

    pwm_speed = 100
    logging.debug("{0}pwm_speed has been set to 100".format(log_time))
    logging.debug("{0}GPIO successfully configured".format(log_time))

except Exception as e:
    logging.error("{0}".format(log_time), e)
    logging.error("{0}Could not setup GPIOs, exiting!".format(log_time))
    sys.exit(-1)


# activate fans
def cooling():
    if not os.path.exists("/home/config/code/python/.kill_cooling.txt"):
        logging.debug("{0}Killswitch does not exist".format(log_time))

        os.mknod("/home/config/code/python/.kill_cooling.txt")
        logging.debug("{0}Sucessfully created killswitch".format(log_time))                   # create killswitch file to show that cooling is active

    GPIO.output(17, 0)
    logging.debug("{0}GPIO Output #17 has been set to 0 = On".format(log_time))
    for pwm_speed in range(255):
        if os.path.exists("/home/config/code/python/.kill_cooling.txt"):        # checking if killswitch exists...
            logging.debug("{0}Killswitch is existing, therefore starting to cool the system...".format(log_time))

            pwm.set_PWM_dutycycle(23, pwm_speed)
            logging.debug("{0}pwm-speed for GPIO Output #23 has been set to the current pwm_speed".format(log_time))

            pwm_speed + 10
            logging.debug("{0}pwm_speed has been increased by 10.".format(log_time))

            time.sleep(10)
            logging.debug("{0}We waited 10s to proceed".format(log_time))
        else:
            logging.debug("{0}Killswitch did exist, stoping cooling...".format(log_time))

            GPIO.output(17, 0)                                                  # ...if not, stop cooling
            logging.debug("{0}GPIO Output #17 has been set to 0".format(log_time))

            pwm.set_PWM_dutycycle(23, 0)
            logging.debug("{0}pwm-speed for GPIO Output #23 has been set to 0".format(log_time))
            logging.debug("{0}Exiting skript... bye!".format(log_time))

            sys.exit(0)

try:
    logging.info("{0}Going to start cooling...".format(log_time))
    cooling()
    logging.debug("{0}started cooling".format(log_time))

except Exception as e:
        logging.error("{0}".format(log_time), e)
        logging.error("{0}Could start cooling, exiting!".format(log_time))
        sys.exit(-1)
