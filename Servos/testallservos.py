# EES a program to test all the servos to make sure they work
# 17/12/19 William Gibbens


import board
import digitalio
import busio
import adafruit_pca9685
from adafruit_servokit import ServoKit
import time


# Set up the servo HAT
pin = digitalio.DigitalInOut(board.D4)
i2c = busio.I2C(board.SCL, board.SDA)
kit = ServoKit(channels=16)
kit.servo[0].actuation_range = 180
print ("set up done")

def servo_test(pin_number):
    kit.servo[pin_number].angle = 180
    time.sleep(1)
    print (pin_number, ": turned to 180")

    kit.servo[pin_number].angle = 90
    time.sleep(10)
    print (pin_number, ": turned to 90")

    kit.servo[pin_number].angle = 0
    time.sleep(1)
    print (pin_number, ": turned to 0")
    print("finished")

while True:
    angle = int(input(": "))
    kit.servo[1].angle = angle
    

