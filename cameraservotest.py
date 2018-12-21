## Find the max left, right, up, and down

#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
pwm = PWM(0x40)
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

UPDOWN=5
LEFTRIGHT=4
CENTERCAMERA=450
MAXLEFT= 680
MAXRIGHT=CENTERCAMERA-100

pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
while (True):
  print "-----------"
  # Change speed of continuous servo on channel O
  pwm.setPWM(LEFTRIGHT, 0, CENTERCAMERA)
  pwm.setPWM(UPDOWN, 0, 450)
  time.sleep(1)
  #pwm.setPWM(LEFTRIGHT, 0, CENTERCAMERA)
  #pwm.setPWM(UPDOWN, 0, 450)
  #time.sleep(1)
  #pwm.setPWM(LEFTRIGHT, 0, MAXRIGHT)
  #pwm.setPWM(UPDOWN, 0, 600)
  #time.sleep(1)
  #pwm.setPWM(LEFTRIGHT, 0, CENTERCAMERA)
  #pwm.setPWM(UPDOWN, 0, 450)
  #time.sleep(1)



