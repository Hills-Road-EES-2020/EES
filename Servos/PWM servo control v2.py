# WG Created: 16/12/19 Modified: 17/12/19
# EES v


import board
import digitalio
import busio
import adafruit_pca9685
from adafruit_servokit import ServoKit
import time

"""
1 4
PWM servo contol v1.py  
3 6
"""
# Configuration
up_angle = 90
down_angle = 180
pause_between_letters = 2
pin_addresses_dict = {1:1, 2:2, 3:4, 4:5, 5:6, 6:7} # {pin_number, servo_address}

# Set up the servo HAT
pin = digitalio.DigitalInOut(board.D4)
i2c = busio.I2C(board.SCL, board.SDA)
kit = ServoKit(channels=16)
kit.servo[0].actuation_range = 180
print ("set up done")



def text_to_braille(text):
    alphabet_dict = {'a': [1], 'b': [1,2], 'c': [1,4], 'd': [1,4,5], 'e': [1,5], 'f': [1,2,4], 'g': [1,2,4,5], 'h': [1,2,5], 'i': [2,4], 'j': [2,4,5], 'k': [1,3], 'l': [1,2,3], 'm': [1,3,4], 'n': [1,3,4,5], 'o': [1,3,5], 'p': [1,2,3,4], 'q': [1,2,3,4,5], 'r': [1,2,3,5], 's': [2,3,4], 't': [2,3,4,5], 'u': [1,3,6], 'v': [1,2,3,6], 'w': [2,4,5,6], 'x': [1,3,4,6], 'y': [1,3,4,5,6], 'z': [1,3,5,6]}
    braille_output = []
    for letter in text:
        braille_output.append(alphabet_dict[letter])
    return braille_output


def servo(pin_number, direction):
    servo_address = pin_addresses_dict[pin_number] # Change the pin number to the servo address
    if direction == "up":
        angle = up_angle
    elif direction == "down":
        angle = down_angle

    kit.servo[servo_address].angle = angle

text = input("Type some text: ")
braille = text_to_braille(text)

for item in braille:
    print(item)
    servo(1, "down")
    servo(2, "down")
    servo(3, "down")
    servo(4, "down")
    servo(5, "down")
    servo(6, "down")
    for pin in item:
        servo(pin, "up")
    time.sleep(pause_between_letters)

"""Initialisation of servos 
servo(1, "down")
servo(2, "down")
servo(3, "down")
servo(4, "down")
servo(5, "down")
servo(6, "down")

servo(1, "up")
servo(2, "up")
servo(3, "up")
servo(4, "up")
servo(5, "up")
servo(6, "up")"""
