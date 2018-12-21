from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from time import sleep
from robotlib import *
from Adafruit_PWM_Servo_Driver import PWM
import cv2

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 15
camera.hflip = True
camera.vflip = True

rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(1)

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



for frame in camera.capture_continuous(rawCapture, format = 'bgr', use_video_port = True):
        image = frame.array
	
	pwm.setPWMFreq(60)
	print "---------"
	#change speed of cont servo on channel 0

	pwm.setPWM(LEFT_RIGHT, 0, MAX_LEFT)
	pwm.setPWM(UP_DOWN, 0, 550)
	time.sleep(2)

	pwm.setPWM(LEFT_RIGHT, 0, 541)
	pwm.setPWM(UP_DOWN, 0, 550)
	time.sleep(2)

	pwm.setPWM(LEFT_RIGHT, 0, 503)
	pwm.setPWM(UP_DOWN, 0, 550)
	time.sleep(2)

	pwm.setPWM(LEFT_RIGHT, 0,465 )
	pwm.setPWM(UP_DOWN, 0, 550)

        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF

        rawCapture.truncate(0)

        if key == ord("q"):
                break

