# /usr/bin/python3
# -*- coding: utf-8 -*-
# from https://github.com/JJandke
#
# "1" stands for "off" and "0" stands for "on", because the relay module I use does not switch when the current is present, but at 0V it does.
# However, I only want current to flow at the relay, when the fan is running.
# Therefore, another wiring is not possible and the problem must be solved on software side.
# With other relay modules it might be that "0" and "1" have to be exchanged. Of course, 0 and 1 can also be replaced by "True" and "False" or "GPIO.HIGH" and "GPIO.LOW".

from gpiozero import CPUTemperature
import RPi.GPIO as GPIO
import os
import time
import logging
import datetime


# Create log file for this script
# Running the script via cronjob at boot will delete the log file each time to save disk space and keep the file more organized.
if os.path.isfile("/home/config/log/cooling_pi.log"):
    os.remove("/home/config/log/cooling_pi.log")
    f = open("/home/config/log/cooling_pi.log", "x")
    f.close()
else:
    f = open("/home/config/log/cooling_pi.log", "x")
    f.close()

logging.basicConfig(filename="/home/config/log/cooling_pi.log", level=logging.DEBUG)


day = datetime.datetime.now()
log_time = day.strftime("%a-%d.%m.%Y-%H:%M:%S ")


try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)  # set setwarnings = False if another script uses the GPIO
    GPIO.setup(4, GPIO.OUT)  # raspberry pi fan
    GPIO.setup(17, GPIO.OUT)  # hdd fan
    logging.debug("{0}GPIO successfully configured".format(log_time))

except Exception as e:
    logging.error("{0}".format(log_time), e)


# test fans
GPIO.output(4, 0)
GPIO.output(17, 0)
time.sleep(10)
GPIO.output(4, 1)
GPIO.output(17, 1)
logging.debug("{0}Tested fans".format(log_time))

# check the CPU temperature
while True:
    day = datetime.datetime.now()
    log_time = day.strftime("%a-%d.%m.%Y-%H:%M:%S ")
    cpu = CPUTemperature()
    cpuStr = str(cpu.temperature)

    # The time intervals during which the cooling takes place should still be adapted to your own setup.
    if cpu.temperature < 40:
        logging.info("{0}Temperature below 40°C => {1}°C".format(log_time, cpuStr))
        GPIO.output(4, 1)
        GPIO.output(17, 1)
        time.sleep(300)  # wait for five minutes

    elif 40 <= cpu.temperature < 50:
        logging.info("{0}Temperature between 40°C and 50°C => {1}°C".format(log_time, cpuStr))
        GPIO.output(4, 0)
        GPIO.output(17, 1)
        time.sleep(300)  # wait for five minutes

    elif 50 <= cpu.temperature < 60:
        logging.info("{0}Temperature between 50°C and 60°C => {1}°C".format(log_time, cpuStr))
        GPIO.output(4, 0)
        GPIO.output(17, 1)
        time.sleep(600)  # wait for ten minutes

    elif 60 <= cpu.temperature <= 80:
        logging.warning("{0}Temperature between 60°C and 80°C => {1}°C".format(log_time, cpuStr))
        GPIO.output(4, 0)
        GPIO.output(17, 1)
        time.sleep(900)  # wait for 15 minutes

    elif cpu.temperature > 80:
        logging.warning("{0}Temperature over 80°C => {1}°C".format(log_time, cpuStr))
        GPIO.output(4, 0)
        GPIO.output(17, 0)  # HDD fan for better air supply
        time.sleep(1200)  # wait for 20 minutes
