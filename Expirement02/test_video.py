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
MAXLEFT=CENTERCAMERA+100
MAXRIGHT=CENTERCAMERA-100

pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
while (True):
  print "-----------"
  # Change speed of continuous servo on channel O
  pwm.setPWM(LEFTRIGHT, 0, MAXLEFT)
  pwm.setPWM(UPDOWN, 0, 300)
  time.sleep(1)
  pwm.setPWM(LEFTRIGHT, 0, CENTERCAMERA)
  pwm.setPWM(UPDOWN, 0, 450)
  time.sleep(1)
  pwm.setPWM(LEFTRIGHT, 0, MAXRIGHT)
  pwm.setPWM(UPDOWN, 0, 600)
  time.sleep(1)
  pwm.setPWM(LEFTRIGHT, 0, CENTERCAMERA)
  pwm.setPWM(UPDOWN, 0, 450)
  time.sleep(1)

