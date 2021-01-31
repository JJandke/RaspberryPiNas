# /usr/bin/python3
# -*- coding: utf-8 -*-
# from https://github.com/JJandke
#
# "1" stands for "off" and "0" stands for "on", because the relay module I use does not switch when the current is present, but at 0V it does.
# However, I only want current to flow at the relay when the fan is running.
# Therefore, another wiring is not possible and the problem must be solved on software side.
# With other relay modules it might be that "0" and "1" have to be exchanged. Of course, 0 and 1 can also be replaced by "True" and "False" or "GPIO.HIGH" and "GPIO.LOW".

from gpiozero import CPUTemperature
from datetime import date
import RPi.GPIO as GPIO
import time
import logging
import os


# Create log file for this script
# If the script is executed via cronjob at boot, the content of the log file will automatically be deleted at each boot to save storage space.
if os.path.isfile("/home/ubuntu/log/cooling_pi.log"):
    os.remove("/home/ubuntu/log/cooling_pi.log")
    f = open("/home/ubuntu/log/cooling_pi.log", "x")
    f.close()
else:
    f = open("/home/ubuntu/log/cooling_pi.log", "x")
    f.close()

logging.basicConfig(filename="/home/ubuntu/log/cooling_pi.log", level=logging.DEBUG)


today = date.today()
log_time = today.strftime("%a, %d.%m.%Y-%H:%M:%S ")


try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)  # set setwarnings = False if another script uses the GPIO
    GPIO.setup(4, GPIO.OUT)  # raspberry pi fan
    GPIO.setup(17, GPIO.OUT)  # hdd fan
    logging.debug("GPIO successfully configured")

except Exception as e:
    logging.error("e")


# test fans
GPIO.output(4, 1)
GPIO.output(17, 1)
time.sleep(3)
GPIO.output(4, 0)
GPIO.output(17, 0)
time.sleep(3)
GPIO.output(4, 1)
GPIO.output(17, 1)
time.sleep(3)
logging.debug("Tested fans")

# check the PIs CPU temperature
while True:
    today = date.today()
    log_time = today.strftime("%a, %d.%m.%Y-%H:%M:%S ")
    cpu = CPUTemperature()
    cpuStr = str(cpu.temperature)

    if cpu.temperature < 40:
        logging.info("{0}Temperature below 40°C => {1}°C".format(log_time, cpuStr))
        GPIO.output(4, 1)
        GPIO.output(17, 1)
        time.sleep(120)  # wait for two minutes

    elif 40 <= cpu.temperature < 50:
        logging.info("{0}Temperature between 40°C and 50°C => {1}°C".format(log_time, cpuStr))
        GPIO.output(4, 0)
        GPIO.output(17, 1)
        time.sleep(240)  # wait for four minutes

    elif 50 <= cpu.temperature < 60:
        logging.info("{0}Temperature between 50°C and 60°C => {1}°C".format(log_time, cpuStr))
        GPIO.output(4, 0)
        GPIO.output(17, 1)
        time.sleep(360)  # wait for six minutes

    elif 60 <= cpu.temperature <= 80:
        logging.warning("{0}Temperature between 60°C and 80°C => {1}°C".format(log_time, cpuStr))
        GPIO.output(4, 0)
        GPIO.output(17, 1)
        time.sleep(600)  # wait for ten minutes

    elif cpu.temperature > 80:
        logging.warning("{0}Temperature over 80°C => {1}°C".format(log_time, cpuStr))
        GPIO.output(4, 0)
        GPIO.output(17, 0)  # HDD fan for better air supply
        time.sleep(1200)  # wait for 20 minutes
