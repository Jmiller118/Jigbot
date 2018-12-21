from Adafruit_PWM_Servo_Driver import PWM
import time
from robotlib import *

pwm = PWM(0X40)

servoMin = 150
servoMax = 600

def setServoPulse(channel, pulse):
	pulseLength = 1000000
	pulseLength /= 60
	print "d% us per period" % pulseLength
	pulseLength /= 4096
	print "d% us per bit" % pulseLength
	pulse *= 1000
	pulse /= pulseLength
	pwm.setPWM(channel, 0, pulse)

camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()

pwm.setPWM(RIGHT_WHEEL, 0, 382)
pwm.setPWM(LEFT_WHEEL, 0, 422)
pwm.setPWM(UP_DOWN, 0, 350)
camera.capture('1test1.jpg')
time.sleep(2)
pwm.setPWM(UP_DOWN, 0, 550)
camera.capture('1test2.jpg')
time.sleep(5)
pwm.setPWM(RIGHT_WHEEL, 0, 422)
pwm.setPWM(LEFT_WHEEL, 0, 382)
pwm.setPWM(UP_DOWN, 0, 350)
camera.capture('1test3.jpg')
time.sleep(2)
pwm.setPWM(UP_DOWN, 0, 550)
camera.capture('1test4.jpg')
time.sleep(5)
pwm.setPWM(UP_DOWN, 0, FLAT)
camera.capture('1test5.jpg')
time.sleep(2)
pwm.setPWM(RIGHT_WHEEL, 0, 0)
pwm.setPWM(LEFT_WHEEL, 0, 0)

	
