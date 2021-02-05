# /usr/bin/python3
# -*- coding: utf-8 -*-
# from https://github.com/JJandke
#
# "1" stands for "off" and "0" stands for "on", because the relay module I use does not switch when the current is present, but at 0V it does.
# However, I only want current to flow at the relay when the fan is running.
# Therefore, another wiring is not possible and the problem must be solved on software side.
# With other relay modules it might be that "0" and "1" have to be exchanged. Of course, 0 and 1 can also be replaced by "True" and "False" or "GPIO.HIGH" and "GPIO.LOW".

import RPi.GPIO as GPIO
import os
import subprocess
import time
import logging
import datetime

# Create log file for this script
# If the script is executed via cronjob at boot, the content of the log file will automatically be deleted at each boot to save storage space.
if os.path.isfile("/home/config/log/cooling_hdd.log"):
    os.remove("/home/config/log/cooling_hdd.log")
    f = open("/home/config/log/cooling_hdd.log", "x")
    f.close()
else:
    f = open("/home/config/log/cooling_hdd.log", "x")
    f.close()

logging.basicConfig(filename="/home/config/log/cooling_hdd.log", level=logging.DEBUG)

day = datetime.datetime.now()
log_time = day.strftime("%a-%d.%m.%Y-%H:%M:%S ")

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)  # set setwarnings = False if another script uses the GPIO
    GPIO.setup(17, GPIO.OUT)  # hdd fan
    logging.debug("{0}GPIO successfully configured".format(log_time))

except Exception as e:
    logging.error("{0}".format(log_time), e)


def get_hddtemp():
    get_sda = subprocess.Popen("/home/config/code/shell/sda_temp.sh", shell=True, stdout=subprocess.PIPE)
    get_sdb = subprocess.Popen("/home/config/code/shell/sdb_temp.sh", shell=True, stdout=subprocess.PIPE)
    get_sdc = subprocess.Popen("/home/config/code/shell/sdc_temp.sh", shell=True, stdout=subprocess.PIPE)
    get_sdd = subprocess.Popen("/home/config/code/shell/sdd_temp.sh", shell=True, stdout=subprocess.PIPE)
    sda = get_sda.stdout.read()
    sdb = get_sdb.stdout.read()
    sdc = get_sdc.stdout.read()
    sdd = get_sdd.stdout.read()
    print(hdd1, hdd2)
    if hdd1 < hdd2:
        highest = hdd2
        print(highest)
    else:
        highest = hdd1
        print(highest)


# hdd1 = 1
# hdd2 = 2
# highest = 30
# test fans
GPIO.output(17, 0)
time.sleep(1)
GPIO.output(17, 1)
time.sleep(1)
GPIO.output(17, 0)
time.sleep(1)
GPIO.output(17, 1)
logging.debug("{0}Tested fans".format(log_time))

# check the hdd temperature
while True:
    day = datetime.datetime.now()
    log_time = day.strftime("%a-%d.%m.%Y-%H:%M:%S ")
    get_hddtemp()

    if highest < 40:
        logging.info("{0}Temperature below 40°C => {1}°C".format(log_time, highest))
        GPIO.output(17, 1)
        time.sleep(300)  # wait for five minutes

    elif 40 <= highest < 50:
        logging.info("{0}Temperature between 40°C and 50°C => {1}°C".format(log_time, highest))
        GPIO.output(17, 1)
        time.sleep(300)  # wait for five minutes

    elif 50 <= highest < 60:
        logging.info("{0}Temperature between 50°C and 60°C => {1}°C".format(log_time, highest))
        GPIO.output(17, 1)
        time.sleep(600)  # wait for ten minutes

    elif 60 <= highest <= 80:
        logging.warning("{0}Temperature between 60°C and 80°C => {1}°C".format(log_time, highest))
        GPIO.output(17, 1)
        time.sleep(900)  # wait for 15 minutes

    elif highest > 80:
        logging.warning("{0}Temperature over 80°C => {1}°C".format(log_time, highest))
        GPIO.output(17, 0)
        time.sleep(1200)  # wait for 20 minutes
