# /usr/bin/python3
# -*- coding: utf-8 -*-
# from https://github.com/JJandke
#
# "1" stands for "off" and "0" stands for "on", because the relay module I use does not switch when the current is present, but at 0V it does.
# However, I only want current to flow at the relay when the fan is running.
# Therefore, another wiring is not possible and the problem must be solved on software side.
# With other relay modules it might be that "0" and "1" have to be exchanged. Of course, 0 and 1 can also be replaced by "True" and "False" or "GPIO.HIGH" and "GPIO.LOW".

from gpiozero import CPUTemperature
# import pigpio
import RPi.GPIO as GPIO
import time
import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)     # set setwarnings = False if another script uses the GPIO
GPIO.setup(4, GPIO.OUT)     # raspberry pi fan
GPIO.setup(17, GPIO.OUT)    # hdd fan
# pi = pigpio.pi()

now = datetime.datetime.now()
cpu = CPUTemperature()

#
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

# check the PIs CPU temperature
print("Temperatur: ", cpu.temperature)
while True:
    if cpu.temperature < 40:
        print("Temperatur unter 40°C")
        GPIO.output(4, 1)
        GPIO.output(17, 1)
        time.sleep(120)     # wait two minutes

    elif 40 <= cpu.temperature < 50:
        print("Temperatur zwischen 40 und 50 ")
        GPIO.output(4, 0)
        GPIO.output(17, 1)
        time.sleep(240)     # wait four minutes

    elif 50 <= cpu.temperature < 60:
        print("Temperatur zwischen 50 und 60 ")
        GPIO.output(4, 0)
        GPIO.output(17, 1)
        time.sleep(360)     # wait six minutes

    elif 60 <= cpu.temperature <= 80:
        print("Temperatur zwischen 60 und 80 ")
        GPIO.output(4, 0)
        GPIO.output(17, 1)
        time.sleep(600)     # wait ten minutes

    elif cpu.temperature > 80:
        print("Temperatur über 80")
        GPIO.output(4, 0)
        GPIO.output(17, 0)  # HDD fan for better air supply
        time.sleep(1200)    # wait 20 minutes
