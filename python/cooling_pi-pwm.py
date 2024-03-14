#!/usr/bin/env python3
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
import pigpio
import logging
import datetime

pwm = pigpio.pi()
update_tmp = 60    # The interval (in seconds) for checking the CPU temperature. A smaller number means shorter updates.

# Create log file for this script
# Running the script via cronjob at boot will delete the log file each time to save disk space and keep the file more organized.
if os.path.isfile("/home/config/log/cooling_pi-pwm.log"):
    os.remove("/home/config/log/cooling_pi-pwm.log")
    f = open("/home/config/log/cooling_pi-pwm.log", "x")
    f.close()
else:
    f = open("/home/config/log/cooling_pi-pwm.log", "x")
    f.close()

logging.basicConfig(filename="/home/config/log/cooling_pi-pwm.log", level=logging.DEBUG)


day = datetime.datetime.now()
log_time = day.strftime("%a-%d.%m.%Y-%H:%M:%S ")


try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)     # set setwarnings = False if another script uses the GPIO
    GPIO.setup(4, GPIO.OUT)     # Pi Relay
    GPIO.setup(27, GPIO.OUT)    # Pi PWM
    GPIO.setup(17, GPIO.OUT)    # HDD Relay
    GPIO.setup(23, GPIO.OUT)    # HDD PWM
    logging.debug("{0}GPIO successfully configured".format(log_time))

except Exception as e:
    logging.error("{0}".format(log_time), e)


# test fan
GPIO.output(4, 0)
GPIO.output(17, 0)
pwm.set_PWM_dutycycle(27, 255)
pwm.set_PWM_dutycycle(23, 255)
time.sleep(30)
GPIO.output(4, 1)
GPIO.output(17, 1)
pwm.set_PWM_dutycycle(27, 0)
pwm.set_PWM_dutycycle(23, 255)
logging.debug("{0}Tested fans".format(log_time))

# check the CPU temperature
while True:
    day = datetime.datetime.now()
    log_time = day.strftime("%a-%d.%m.%Y-%H:%M:%S ")
    cpu = CPUTemperature()
    cpuStr = str(cpu.temperature)

    # Since my fans only rotate when the PWM signal exceeds 100, the percentage does not match the used percentage of the PWM signal.
    # I assumed in the calculation 100 = 0%.
    # Therefore, for example, PWM 139 is only 25%, since it represents 25% of the "usable" PWM range [100 - 255 meaning 0% - 100%].
    # Depending on the fan model, the values must still be adjusted.
    if cpu.temperature < 40:
        logging.info("{0}\tCPU Temperature below 40°C => {1}°C\tPi:15%  HDD: 0%".format(log_time, cpuStr))
        GPIO.output(4, 0) # Pi-Relay On
        GPIO.output(17, 1) # HDD-Relay Off
        pwm.set_PWM_dutycycle(27, 123) # Pi-PWM 15%
        pwm.set_PWM_dutycycle(23, 0) # HDD-PWM 0%
        time.sleep(update_tmp)

    elif 40 <= cpu.temperature < 45:
        #logging.info("{0}\tCPU Temperature is {1}°C\tPi:35%  HDD: 75%".format(log_time, cpuStr))
        logging.info("{0}\tCPU Temperature is {1}°C\tPi:35%  HDD: OFF".format(log_time, cpuStr))
        GPIO.output(4, 0) # Pi-Relay On
        GPIO.output(17, 1) # Anpassung um HDD Kühlung auszuschalten, default Wert = 0
        pwm.set_PWM_dutycycle(27, 154)
        pwm.set_PWM_dutycycle(23, 238)
        time.sleep(update_tmp)

    elif 45 <= cpu.temperature < 50:
        #logging.info("{0}\tCPU Temperature is {1}°C\tPi:50%  HDD: 75%".format(log_time, cpuStr))
        logging.info("{0}\tCPU Temperature is {1}°C\tPi:50%  HDD: OFF".format(log_time, cpuStr))
        GPIO.output(4, 0) # Pi-Relay On
        GPIO.output(17, 1) # Anpassung um HDD Kühlung auszuschalten, default Wert = 0
        pwm.set_PWM_dutycycle(27, 177)
        pwm.set_PWM_dutycycle(23, 238)
        time.sleep(update_tmp)

    elif 50 <= cpu.temperature <= 60:
        logging.info("{0}\tCPU Temperature is {1}°C\tPi:75%  HDD: 75%".format(log_time, cpuStr))
        GPIO.output(4, 0) # Pi-Relay On
        GPIO.output(17, 0) # HDD-Relay On
        pwm.set_PWM_dutycycle(27, 216) # Pi-PWM 75%
        pwm.set_PWM_dutycycle(23, 238) # HDD-PWM 75%
        time.sleep(update_tmp)

    elif 60 <= cpu.temperature <= 70:
        logging.info("{0}\tCPU Temperature is {1}°C\tPi:85%  HDD: 80%".format(log_time, cpuStr))
        GPIO.output(4, 0)
        GPIO.output(17, 0)
        pwm.set_PWM_dutycycle(27, 231)
        pwm.set_PWM_dutycycle(23, 244)
        time.sleep(update_tmp)

    elif cpu.temperature > 80:
        logging.info("{0}\tCPU Temperature is {1}°C\tPi:100%  HDD: 100%".format(log_time, cpuStr))
        GPIO.output(4, 0)
        GPIO.output(17, 0)
        pwm.set_PWM_dutycycle(27, 255)
        pwm.set_PWM_dutycycle(23, 255)
        time.sleep(update_tmp)
