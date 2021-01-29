# usr/bin/python3
print(">> import data...")
from gpiozero import CPUTemperature
import pigpio
import RPi.GPIO as GPIO
import time
import datetime
print("   - done")

#time.sleep(0.5)
print(">> setup packages...")
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12,GPIO.OUT) #led_relay
GPIO.setup(25,GPIO.OUT) #fan2
GPIO.setup(19,GPIO.OUT) #fan1
pi = pigpio.pi()
now = datetime.datetime.now()
print("   - done")

#time.sleep(0.5)
print(">> searching for CPU temperature...")
cpu = CPUTemperature()
print("   -", cpu.temperature, "°C")
print(">> searching for datetime...")
print(time.strftime("   - %d.%m.%Y %H:%M:%S"))
print("   - done")

#time.sleep(0.5)
print(">> checking relay...")
GPIO.output(19,GPIO.HIGH)
print("   - fan1 = HIGH")
time.sleep(3)
GPIO.output(25,GPIO.HIGH)
print("   - fan2 = HIGH")
time.sleep(3)
GPIO.output(19,GPIO.LOW)
print("   - fan1 = LOW")
time.sleep(0.5)
GPIO.output(25,GPIO.LOW)
print("   - fan2 = LOW")
time.sleep(0.5)
GPIO.output(19,GPIO.HIGH)
print("   - fan1 = HIGH")
time.sleep(3)
GPIO.output(25,GPIO.HIGH)
print("   - fan2 = HIGH")
time.sleep(3)
GPIO.output(19,GPIO.LOW)
print("   - fan1 = LOW")
time.sleep(0.5)
GPIO.output(25,GPIO.LOW)
print("   - fan2 = LOW")
time.sleep(0.5)

while True:
    if cpu.temperature < 50:
        GPIO.output(19,GPIO.LOW)
        GPIO.output(25,GPIO.LOW)
        #print("Ok")
        time.sleep(300)

    elif cpu.temperature >= 50 and cpu.temperature < 55:
        GPIO.output(19,GPIO.HIGH)
        print(time.strftime('!  %d.%m.%Y %H:%M:%S ') + str(cpu.temperature))
        print(".")
        time.sleep(300)
    elif cpu.temperature >= 55 and cpu.temperature <63:
        GPIO.output(25,GPIO.HIGH)
        print(time.strftime('!  %d.%m.%Y %H:%M:%S ') + str(cpu.temperature))
        print(".")
        time.sleep(300)

    elif cpu.temperature >= 63 and cpu.temperature <= 80:
        GPIO.output(25,GPIO.HIGH)
        GPIO.output(19,GPIO.HIGH)
        print(time.strftime('!  %d.%m.%Y %H:%M:%S ') + str(cpu.temperature))
        print(".")
        time.sleep(200)



    elif cpu.temperature > 80:

        GPIO.output(25, GPIO.HIGH)

        GPIO.output(26, GPIO.HIGH)

        GPIO.output(12, GPIO.HIGH)

        print(time.strftime('!  %d.%m.%Y %H:%M:%S ') + str(cpu.temperature))

        print(cpu.temperature)

        print("What the Hell are you doin, that your RaspberryPi gets that hot?!")

        i = 400

        while i > 0:
            pi.set_PWM_dutycycle(16, 250)

            time.sleep(1)

            pi.set_PWM_dutycycle(16, 0)

            time.sleep(1)

            i = i - 1

    if cpu.temperature < 10:
        print(cpu.temperature)

    ##    else:

    ##        print("oops, something went wrong, try to restart the software or reboot!")




