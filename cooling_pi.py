# usr/bin/python3

from gpiozero import CPUTemperature
import pigpio
import RPi.GPIO as GPIO
import time
import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT)  # raspberry pi fan
pi = pigpio.pi()

now = datetime.datetime.now()
cpu = CPUTemperature()

GPIO.output(4, GPIO.HIGH)
time.sleep(3)
GPIO.output(4, GPIO.LOW)
time.sleep(3)
GPIO.output(4, GPIO.HIGH)
time.sleep(3)
GPIO.output(4, GPIO.LOW)

while True:
    if cpu.temperature < 40:
        GPIO.output(4, GPIO.LOW)
        time.sleep(300)

    elif 40 <= cpu.temperature < 50:
        GPIO.output(4, GPIO.HIGH)
        time.sleep(200)

    elif 50 <= cpu.temperature < 60:
        GPIO.output(4, GPIO.HIGH)
        time.sleep(300)

    elif 60 <= cpu.temperature <= 80:
        GPIO.output(4, GPIO.HIGH)
        time.sleep(600)

    elif cpu.temperature > 80:
        GPIO.output(4, GPIO.HIGH)
