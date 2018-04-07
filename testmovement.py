# Controlling it with rpi
# possibly import in function even tho it is wrong convention
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

# Initializes the 3 pins
# pin CW
CW
# pin CCW
CCW
# pin On/Off
onAndOff

GPIO.setup(CW,GPIO.OUT)
GPIO.setup(CCW,GPIO.OUT)
GPIO.setup(onAndOff,GPIO.OUT)

# Movement going CW
GPIO.output(CW,GPIO.HIGH)
GPIO.output(CCW,GPIO.LOW)
GPIO.output(onAndOff,GPIO.HIGH)

# time.sleep using using arf to calculate time to move specific distance

sleep(calculateTime)

# Movement going CCW
GPIO.output(CW,GPIO.LOW)
GPIO.output(CCW,GPIO.HIGH)
GPIO.output(onAndOff,GPIO.HIGH)

# Next calculation // Maybe split into second function

# movement ending

GPIO.output(onAndOff,GPIO.LOW)

GPIO.cleanup()




