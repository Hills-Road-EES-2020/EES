# WG Created: 16/12/19 Modified: 17/12/19
# EES Servo control version 3 - added suppport for more customisable pin angles


import board
import digitalio
import busio
import adafruit_pca9685
from adafruit_servokit import ServoKit
import time

"""
1 4
2 5
3 6
"""

# Configuration
down_angle_default = 90 # angle of the servo when in the up position
up_angle_default = 180 # angle of the servo when in the down position
pause_between_letters = 2 # seconds to wait between each outputted letter

# Set up the servo HAT
pin = digitalio.DigitalInOut(board.D4)
i2c = busio.I2C(board.SCL, board.SDA)
kit = ServoKit(channels=16)
kit.servo[0].actuation_range = 180

# Functions
def text_to_braille(text):
    """(text) - Outputs a list of the pin numbers for each character given"""
    alphabet_dict = {'a': [1], 'b': [1,2], 'c': [1,4], 'd': [1,4,5], 'e': [1,5], 'f': [1,2,4], 'g': [1,2,4,5], 'h': [1,2,5], 'i': [2,4], 'j': [2,4,5], 'k': [1,3], 'l': [1,2,3], 'm': [1,3,4], 'n': [1,3,4,5], 'o': [1,3,5], 'p': [1,2,3,4], 'q': [1,2,3,4,5], 'r': [1,2,3,5], 's': [2,3,4], 't': [2,3,4,5], 'u': [1,3,6], 'v': [1,2,3,6], 'w': [2,4,5,6], 'x': [1,3,4,6], 'y': [1,3,4,5,6], 'z': [1,3,5,6]}
    braille_output = []
    for letter in text:
        braille_output.append(alphabet_dict[letter])
    return braille_output  

def servo(pin_number, direction):
    """(pin_number, direction) - moves the servo specified to the given direction"""
    servo_address == pin_number - 1 # Change the pin number to the servo address
    
    if direction == down: # list of conditional statements to set the correct angle for the servo
        angle = down_angle_default
    elif direction == up:
        angle = up_angle_default
    else:
        angle = down_angle_default

    kit.servo[servo_address].angle = angle


text = "test"
braille = text_to_braille(text)

for item in braille:
    print(item)
    servo(1, down)
    servo(2, down)
    servo(3, down)
    servo(4, down)
    servo(5, down)
    servo(6, down)
    for pin in item:
        servo(pin, up)
    time.sleep(pause_between_letters)
    
