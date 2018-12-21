## Move if dot is halfway there, else just stop

# import the necessary packages
from Adafruit_PWM_Servo_Driver import PWM
from robotlib import *
from collections import deque
from math import pi, sqrt
import numpy as np
import argparse
import imutils
import math
import cv2


def angle_between(p0, p1, p2):
    v0 = np.array(p0) - np.array(p1)
    v1 = np.array(p2) - np.array(p1)
    
    angle = np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1))
    return angle
 
def setLeftVelocity(self, v):
    d = self.distanceToTarget()
    if (d > 200):
       	s = 4
    else:
        s = d/200 * 4
            
    v = v/10
    if v > 1: v = 1
    elif v < -1 : v = -1
       
    self.leftWheelVelocity = s + v
       
    if self.leftWheelVelocity < 0: self.leftWheelVelocity = 0
    
def setRightVelocity(self, v):
    d = self.distanceToTarget()
    if (d > 200):
    	s = 4
    else:
        s = d/200 * 4
        
    v = v/10
    if v > 1: v = 1
    elif v < -1 : v = -1
        
    self.rightWheelVelocity = s + v
        
    if self.rightWheelVelocity < 0: self.rightWheelVelocity = 0

def distanceToTarget(self):
        return distance((self.cx, self.cy),
                        (self.target.cx, self.target.cy))

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
bgr = np.uint8([[[0, 0, 0]]])
targetColor = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
diff = (30, 15, 15)
greenLower = targetColor - diff
greenUpper = targetColor + diff

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()

	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	retval, frame = cv2.threshold(frame, 50, 255, cv2.THRESH_BINARY)
	frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]

	# print "cnts = ", cnts

	x_max = frame.shape[1]
	y_max = frame.shape[0]
	
	p0 = (x_max / 2, y_max)
	p1 = (x_max / 2, 0)

	# "robot"
	cv2.circle(frame, p1, 20, (0, 0, 255), -1)
	
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)

		
		# only proceed if the radius meets a minimum size
		if radius > 10:
			
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			
			# (x,y) is center of circle
			cv2.circle(frame, (int(x),int(y)), 5, (0, 255, 0), -1)
			cv2.line(frame, (0, (y_max /2 )), (x_max, y_max/2), (210, 70, 10), 5)
			#cv2.circle(frame, p0, 20, (0, 255, 0), -1)
			#print("p1 is ", p1)
			#angle = math.atan2((x_max - int(x)), (y_max - int(y)))
			angle = angle_between(p0,p1,(x,y))
			dist_to_circle = sqrt(pow(p1[0] - x, 2) + pow(p1[1] - y, 2)) - radius
			print("dist to circ ", dist_to_circle) 
			
			if dist_to_circle > (y_max / 2):
				pwm.setPWM(RIGHT_WHEEL, 0, 317)
				pwm.setPWM(LEFT_WHEEL, 0, 355)

			else:
				pwm.setPWM(RIGHT_WHEEL, 0, 0)
				pwm.setPWM(LEFT_WHEEL, 0, 0)
			
			
			
			#print("angle is : ", angle, 180/ pi * angle) 
						

	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
