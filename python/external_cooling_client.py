#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from https://github.com/JJandke

import datetime
import requests
import logging
import time
import sys
import os


try:
    logging.basicConfig(filename="/home/config/log/request_cooling.log", level=logging.DEBUG)
    now = datetime.datetime.now()
    log_time = now.strftime("%a-%d.%m.%Y-%H:%M:%S ")

except Exception as e:
    print(e)
    print("FATAL ERROR! - Could not set up logging, exiting!")
    sys.exit(-1)


# Create log file if it does not exist.
try:
    if not os.path.isfile("/home/config/log/request_cooling.log"):
        logging.debug("{0}Logfile does not exist, therefore we will create it...".format(log_time))
        f = open("/home/config/log/request_cooling.log", "x")
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



update_tmp = 60
logging.debug("{0}Set update_tmp to 60 seconds".format(log_time))

while True:
    day = datetime.datetime.now()
    log_time = day.strftime("%a-%d.%m.%Y-%H:%M:%S ")
    logging.debug("{0}Datetine for logging has again been set, because we're in a endless loop".format(log_time))

    cpu_temp = float(os.popen('vcgencmd measure_temp| sed "s/[^0-9.]//g" ').readline())
    logging.debug("{0}We received the CPU-Temperature".format(log_time))

    cpuStr = str(cpu_temp)
    logging.debug("{0}We converted the CPU-Temperature as String for logging.".format(log_time))

    if cpu_temp < 50:
        logging.debug("{0}\tCPU Temperature below 50°C => {1}°C, nothing to do".format(log_time, cpuStr))
        time.sleep(update_tmp)

    elif cpu_temp >= 50:
        logging.info("{0}\tCPU Temperature is {1}°C, requesting cooling".format(log_time, cpuStr))
        r = requests.get("http://rpi-nas/start_cooling.php")
        logging.debug("{0}Requested URL, now sleeping".format(log_time))
        time.sleep(update_tmp)
        logging.debug("{0}Slept for log_time seconds.".format(log_time))

        while cpu_temp >= 50:
            logging.debug("{0}CPU-Temperature still > 50°C, sleeping".format(log_time))
            time.sleep(update_tmp)
            logging.debug("{0}Slept again for log_time seconds".format(log_time))

        logging.debug("{0}CPU-Temperature now < 50°C, requesting to stop cooling".format(log_time))
        s = requests.get("http://rpi-nas/stop_cooling.php")
        logging.debug("{0}Requested to stop cooling".format(log_time))


    else:
        logging.info("{0}\tSomething fucked up... Exiting!".format(log_time))
        sys.exit(-1)
