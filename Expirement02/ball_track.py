#import what we need
from collections import deque
import numpy as np
import argparse 
import imutils
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from time import sleep
from robotlib import *
from Adafruit_PWM_Servo_Driver import PWM

camera = PiCamera()
#camera.resolution = (640, 480)
#camera.framerate = 32
camera.hflip = True
camera.vflip = True

#rawCapture = PiRGBArray(camera, size=(640, 480))

#time.sleep(1)

#for frame in camera.capture_continuous(rawCapture, format = 'bgr', use_video_port = True):
 #      frame = frame.array

#       cv2.imshow("Frame", frame)
#       key = cv2.waitKey(1) & 0xFF

#       rawCapture.truncate(0)

#      if key == ord("q"):
#               break

#construct the arguement parse
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help = "path to the video file", action = 'store_true')
ap.add_argument("-b", "--buffer", type = int, default = 64,  help = "max buffer size")
args = vars(ap.parse_args())


greenLower = (0,0,0)
greenUpper = (0, 0, 0)
pts = deque(maxlen=args["buffer"])

# and upper bound of the "green"
#ball in the HSV color space, then initalize to webcam

if not args.get("video", False):
	camera = cv2.VideoCapture(0)

#otherwise, grab ref to video file
else:
	camera = cv2.VideoCapture(args["video"])


#keeip looking!
while True:
	#grab the current frame
	(grabbed, frame) = camera.read()
	#ret, frame = camera.read()

	#if we are viewing a video and did not grab a frame,
	#we have the end of the video

	##overflow answer
	#if not grabbed:
	#	continue
	
	#blog guy code	
	if args.get("video") and not grabbed:
		break

	#resize the frame, blur, and convert to HSV color
	frame = imutils.resize(frame, width = 600)
	#blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	#construct a mask for the color "green"
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations = 2)
	mask = cv2.dilate(mask, None, iterations = 2)

	#find contours and the center
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = none

	#only keep going if at least one was found
	if len(cnts) > 0:
		#find the largest
		c = max(cnts, key = cv2.contourArea)
		((x,y), radius) = cv2.minEnclosingCirlce(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		#only proceed if radius is met
		if radius > 5:
			#draw a cirlce
			cv2.cirle(frame, (int(x), int(y)), int(radius), (0,255, 255), 2)
			cv2.cirlce(frame, center, 5, (0,0,255),-1)

	pts.appendleft(center)

	#loop over the set of tracked points
	for i in xrange(1, len(pts)):
		#if either of the tracked are None, ignore
		if pts[i-1] is None or pts[i] is None:
			continue

		#else compute thickness of the line
		thickness = int(np.sqrt(args["buffer"] / float(i+1)) * 2.5)
		cv2.line(frame, pts[i-1], pts[i], (0,0, 255), thickness)

	#show the frame
	key = cv2.waitKey(1) & 0xFF
	
	#if q is pressed
	if key == ord("q"):
		break

#cleanup the camera and close it

#cv2.imshow('frame', frame)
camera.release()
cv2.destroyAllWindows()
