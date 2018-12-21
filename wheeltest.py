#!/usr/bin/python

#from Adafruit_PWM_Servo_Driver import PWM
import time
from robotlib import *

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
#pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

#pwm.setPWMFreq(60)                        # Set frequency to 60 Hz

# Change speed of continuous servo on channel O

#for x in range(300, 302):
	#print "---------------", x
	#pwm.setPWM(0, 0, x)
	#pwm.setPWM(1, 0, x)
	# time.sleep(2)

#time.sleep(3)
pwm.setPWM(RIGHT_WHEEL, 0, 382)
pwm.setPWM(LEFT_WHEEL, 0, 422)
time.sleep(2)
pwm.setPWM(RIGHT_WHEEL, 0, 382)
pwm.setPWM(LEFT_WHEEL, 0, 0)
time.sleep(2)
pwm.setPWM(RIGHT_WHEEL, 0, 422)
pwm.setPWM(LEFT_WHEEL, 0, 382)
time.sleep(2)
pwm.setPWM(RIGHT_WHEEL, 0, 0)
pwm.setPWM(LEFT_WHEEL, 0, 0)



