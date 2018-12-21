#from gpiozero import Robot, DigitalInputDevice
from robotlib import *
from Adafruit_PWM_Servo_Driver import PWM
from time import sleep

class Encoder(object):
	def __init__(self, pin):
		self._value = 0
		encoder = DigitalInputDevice(pin)
		encoder.when_activated  = self._increment
		encoder.when_deactivated = self._increment

	def reset(self):
		self._value = 0
	def _increment(self):
		self._value = 1
	def value(self):
		return self._value

##may have to change later
##LF, LB, RF, RB

SAMPLETIME = 1

r = pwm.setPWM(RIGHT_WHEEL), pwm.setPWM(LEFT_WHEEL)
e1 = Encoder(0)
e2 = Encoder(1)

m1_speed = 1.0
m2_speed = 1.0
r.value = (m1_speed, m2_speed)

while True:
	print "e1 {} e2 {}".format(e1.value, e2.value)
	sleep(SAMPLETIME)
