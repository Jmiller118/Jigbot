from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from time import sleep
from robotlib import *
from Adafruit_PWM_Servo_Driver import PWM
import cv2

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
camera.hflip = True
camera.vflip = True

rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(1)

for frame in camera.capture_continuous(rawCapture, format = 'bgr', use_video_port = True):
	image = frame.array

	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
	
	rawCapture.truncate(0)

	if key == ord("q"):
		break


#initialise using defalt address
pwm = PWM(0X40)
for frame in camera.capture_continuous(rawCapture, format = 'bgr', use_video_port = True):
        image = frame.array

        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF

        rawCapture.truncate(0)

        if key == ord("q"):
                break


