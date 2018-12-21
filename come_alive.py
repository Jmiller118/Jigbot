from Adafruit_PWM_Servo_Driver import PWM
import time
from robotlib import *

#initialize pwm using default
pwm = PWM(0X40)

servoMin = 150
servoMax = 600

def setServoPulse(channel, pulse):
        pulseLength = 1000000
        pulseLength /= 60
        print "%d us per period" % pulseLength
        pulseLength /= 4096
        print "%d us per bit" % pulseLength
        pulse *= 1000
        pulse /= pulseLength
        pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(60)
time.sleep(3)

#initialize pwm using default
pwm = PWM(0X40)

servoMin = 150
servoMax = 600

def setServoPulse(channel, pulse):
        pulseLength = 1000000
        pulseLength /= 60
        print "%d us per period" % pulseLength
        pulseLength /= 4096
        print "%d us per bit" % pulseLength
        pulse *= 1000
        pulse /= pulseLength
        pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(60)

#set camera middle
pwm.setPWM(LEFT_RIGHT, 0, 429)
pwm.setPWM(UP_DOWN, 0, 450)

#travel forward
pwm.setPWM(RIGHT_WHEEL, 0, 379)
pwm.setPWM(LEFT_WHEEL, 0, 424)
time.sleep(3)

#look right
pwm.setPWM(LEFT_RIGHT, 0,579)
pwm.setPWM(UP_DOWN, 0, 450)

#pause
pwm.setPWM(RIGHT_WHEEL, 0, 0)
pwm.setPWM(LEFT_WHEEL, 0, 0)
time.sleep(2)

#make a right turn
pwm.setPWM(RIGHT_WHEEL, 0, 382)
pwm.setPWM(LEFT_WHEEL, 0, 0)
time.sleep(2)

#camera back to middle
pwm.setPWM(LEFT_RIGHT, 0, 429)
pwm.setPWM(UP_DOWN, 0, 450)

#go forward
pwm.setPWM(RIGHT_WHEEL, 0, 379)
pwm.setPWM(LEFT_WHEEL, 0, 422)
time.sleep(2)

#pause
pwm.setPWM(RIGHT_WHEEL, 0, 0)
pwm.setPWM(LEFT_WHEEL, 0, 0)
time.sleep(1)

#look up and down
pwm.setPWM(LEFT_RIGHT, 0, CENTER_CAMERA)
pwm.setPWM(UP_DOWN, 0, 450)
time.sleep(1)
pwm.setPWM(LEFT_RIGHT, 0, CENTER_CAMERA)
pwm.setPWM(UP_DOWN, 0, 600)
time.sleep(1)
pwm.setPWM(LEFT_RIGHT, 0, CENTER_CAMERA)
pwm.setPWM(UP_DOWN, 0, 450)
time.sleep(1)
pwm.setPWM(LEFT_RIGHT, 0, CENTER_CAMERA)
pwm.setPWM(UP_DOWN, 0, 600)
time.sleep(1)
pwm.setPWM(LEFT_RIGHT, 0,CENTER_CAMERA )
pwm.setPWM(UP_DOWN, 0, 450)
time.sleep(3)

#go backwards
pwm.setPWM(RIGHT_WHEEL, 0, 424)
pwm.setPWM(LEFT_WHEEL, 0, 379)
time.sleep(3)

#turn
pwm.setPWM(RIGHT_WHEEL, 0, 0)
pwm.setPWM(LEFT_WHEEL, 0, 422)
time.sleep(2)

#travel forward
pwm.setPWM(RIGHT_WHEEL, 0, 379)
pwm.setPWM(LEFT_WHEEL, 0, 424)
time.sleep(2)

#stop
pwm.setPWM(RIGHT_WHEEL, 0, 0)
pwm.setPWM(LEFT_WHEEL, 0, 0)
time.sleep(2)


