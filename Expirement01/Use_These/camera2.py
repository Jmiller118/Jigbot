from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from time import sleep
from robotlib import *
from Adafruit_PWM_Servo_Driver import PWM
import cv2

camera = PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 30
camera.hflip = True
camera.vflip = True
    

#initialise using defalt address
pwm = PWM(0X40)

servoMin = 150
servoMax = 600

def setServoPulse(channel, pulse):
	pulseLength = 1000000
	pulseLength /= 60
	print "%d us per period" % pulseLength
	pulseLength /= 4096
	print "d% us per bit" % pulseLength
	pulse *= 1000
	pulse /= pulseLength
	pwm.setPWM(channel, 0, pulse)



pwm.setPWMFreq(60)
print "---------"
#change speed of cont servo on channel 0

#pwm.setPWM(LEFT_RIGHT, 0, CENTER_CAMERA)
#pwm.setPWM(UP_DOWN, 0, 450)
#camera.capture('circle_size00.jpg')
#time.sleep(2)

#pwm.setPWM(LEFT_RIGHT, 0, CENTER_CAMERA)
#pwm.setPWM(UP_DOWN, 0, 600)
#camera.capture('000001.jpg')
#time.sleep(2)

#pwm.setPWM(LEFT_RIGHT, 0, CENTER_CAMERA)
#pwm.setPWM(UP_DOWN, 0, 450)
#camera.capture('ball.jpg')
#time.sleep(2)

pwm.setPWM(LEFT_RIGHT, 0, CENTER_CAMERA)
pwm.setPWM(UP_DOWN, 0, 650)
#camera.capture('circle_size04.jpg')
#time.sleep(2)


#pwm.setPWM(LEFT_RIGHT, 0,CENTER_CAMERA )
#pwm.setPWM(UP_DOWN, 0, 450)
#camera.capture('000004.jpg')
#time.sleep(2)
