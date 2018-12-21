
# import the necessary packages
from Adafruit_PWM_Servo_Driver import PWM
from robotlib import *

x = 12

pwm.setPWM(RIGHT_WHEEL, 0, 402 - x)
pwm.setPWM(LEFT_WHEEL, 0, 402 + x)

raw_input("stop")

pwm.setPWM(RIGHT_WHEEL, 0, RIGHT_ZERO)
pwm.setPWM(LEFT_WHEEL, 0, LEFT_ZERO)
