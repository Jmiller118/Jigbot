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

time.sleep(3)
pwm.setPWM(RIGHT_WHEEL, 0, 317)
pwm.setPWM(LEFT_WHEEL, 0, 355)
time.sleep(5)
pwm.setPWM(RIGHT_WHEEL,0, 357)
pwm.setPWM(LEFT_WHEEL, 0, 315)
time.sleep(5)
pwm.setPWM(RIGHT_WHEEL, 0, 0)
pwm.setPWM(LEFT_WHEEL, 0, 0)




