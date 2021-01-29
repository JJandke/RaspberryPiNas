# /usr/bin/python3
# -*- coding: utf-8 -*-
# from https://github.com/JJandke

from gpiozero import CPUTemperature
import pigpio
import RPi.GPIO as GPIO
import time
import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)     # set setwarnings = False if another script uses the GPIO
GPIO.setup(4, GPIO.OUT)     # raspberry pi fan
GPIO.setup(17, GPIO.OUT)    # hdd fan
pi = pigpio.pi()

now = datetime.datetime.now()
cpu = CPUTemperature()

# test fans
GPIO.output(4, GPIO.HIGH)
time.sleep(3)
GPIO.output(4, GPIO.LOW)
time.sleep(3)
GPIO.output(4, GPIO.HIGH)
time.sleep(3)
GPIO.output(4, GPIO.LOW)

# check the PIs CPU temperature
while True:
    if cpu.temperature < 40:
        GPIO.output(4, GPIO.LOW)
        time.sleep(120)     # wait two minutes

    elif 40 <= cpu.temperature < 50:
        GPIO.output(4, GPIO.HIGH)
        time.sleep(240)     # wait four minutes

    elif 50 <= cpu.temperature < 60:
        GPIO.output(4, GPIO.HIGH)
        time.sleep(360)     # wait six minutes

    elif 60 <= cpu.temperature <= 80:
        GPIO.output(4, GPIO.HIGH)
        time.sleep(600)     # wait ten minutes

    elif cpu.temperature > 80:
        GPIO.output(4, GPIO.HIGH)
        GPIO.output(17, GPIO.HIGH)  # HDD fan for better air supply
        time.sleep(1200)    # wait 20 minutes
