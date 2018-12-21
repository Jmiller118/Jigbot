import cv2
import numpy as np
import sys
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from time import sleep
from robotlib import *
from Adafruit_PWM_Servo_Driver import PWM

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
camera.hflip = True
camera.vflip = True

rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(1)


cap = cv2.VideoCapture(0)

for frame in camera.capture_continuous(rawCapture, format = 'bgr', use_video_port = True):
        image = frame.array

        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF

        rawCapture.truncate(0)

        if key == ord("q"):
                break

	while(cap.isOpened()):
#while(True):
	
		ret, frame = cap.read()

		if ret:
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			#gray = cv2.medianBlur(cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY), 5)

			circles = cv2.HoughCirlces(gray, cv2.HOUGH_GRADIENT, 1, 10)# ret = [[Xpos, Ypos, Radius], ...]

			if circles!=None:print "Cirlce there!"
			cv2.imshow('frame', gray)
			
			if cv2.waitKey(1) & 0xFF == ord('q'):
			#if cv2.waitKey(1) == 27:# esc Key
				break


			# Read image
			im = cv2.imread("blob.jpg", cv2.IMREAD_GRAYSCALE)

			# Setup SimpleBlobDetector parameters.
			params = cv2.SimpleBlobDetector_Params()

			# Change thresholds
			params.minThreshold = 10
			params.maxThreshold = 200 
    

			# Filter by Area.
			params.filterByArea = True 
			params.minArea = 1500
    
			# Filter by Circularity
			params.filterByCircularity = True
	
			# Filter by Convexity
			params.filterByConvexity = True
			params.minConvexity = 0.87

			# Filter by Inertia
			params.filterByInertia = True
			params.minInertiaRatio = 0.01

			# Create a detector with the parameters
			ver = (cv2.__version__).split('.')
			if int(ver[0]) < 3 :	
			        detector = cv2.SimpleBlobDetector(params)
			else :
			        detector = cv2.SimpleBlobDetector_create(params)

			
			# Detect blobs.
			keypoints = detector.detect(im)

			# Draw detected blobs as red circles.
			# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
			# the size of the circle corresponds to the size of blob

			im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

			# Show blobs


cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)
#cap.release()
#cv2.destroyAllWindows()
