#!/usr/bin/python

from pid_controller_3.pid import PID, twiddle
from robotlib import *
from Adafruit_PWM_Servo_Driver import PWM
import cv2
import numpy as np
from math import sqrt
import imutils
from time import time

#https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python
def angle_between(p0, p1, p2):
    v0 = np.array(p0) - np.array(p1)
    v1 = np.array(p2) - np.array(p1)
    
    angle = np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1))
    return angle

def distance(a, b):
    s = [pow(ai - bi, 2) for ai, bi in zip(a,b)]
    return sqrt(sum(s))

class Robot(object):
	WHEEL_PWM_MAX = 12

	def __init__(self, camera):
		self.camera = camera
		self.camera.pwm_tilt = 630

		self.wheelRadius = 66.675 # mm
		self.leftPWM = LEFT_ZERO
		self.rightPWM = RIGHT_ZERO
		self.error = 0

		pwm.setPWM(LEFT_RIGHT, 0, CENTER_CAMERA + 10)
		pwm.setPWM(UP_DOWN, 0, self.camera.pwm_tilt)
	
	def setWheelPWM(self, leftCorrection, rightCorrection):
		
		maxDist = self.camera.y_max/2  

		d = self.camera.distanceToTarget()

		if d == None:
			leftSpeed = 0 
			rightSpeed = 0
			leftCorrection = 0
			rightCorrection = 0

		elif d > maxDist:
			leftSpeed = self.WHEEL_PWM_MAX
			rightSpeed = self.WHEEL_PWM_MAX
		
	#	elif d <= 100:
	#		leftSpeed = 1
	#		rightSpeed = -1
		
		else:
			leftSpeed = d/maxDist * self.WHEEL_PWM_MAX
			rightSpeed = d/maxDist * self.WHEEL_PWM_MAX

			
		leftCorrection = leftCorrection / 10
		if leftCorrection > self.WHEEL_PWM_MAX : leftCorrection = self.WHEEL_PWM_MAX
		elif leftCorrection < -self.WHEEL_PWM_MAX : leftCorrection = -self.WHEEL_PWM_MAX
			
		rightCorrection = rightCorrection / 10
		if rightCorrection > self.WHEEL_PWM_MAX : rightCorrection = self.WHEEL_PWM_MAX
		elif rightCorrection < -self.WHEEL_PWM_MAX : rightCorrection = -self.WHEEL_PWM_MAX
		
		self.leftPWM = LEFT_ZERO + leftSpeed + leftCorrection
		self.rightPWM = RIGHT_ZERO - rightSpeed - rightCorrection
		print "leftspped", leftSpeed, "rightspeed", rightSpeed, "leftCorr", leftCorrection, "rightCorr", rightCorrection

		if self.leftPWM < LEFT_ZERO: self.leftPWM = LEFT_ZERO 
		
		if self.rightPWM > RIGHT_ZERO: self.rightPWM = RIGHT_ZERO

	def setLeftPWM(self, p):

		maxDist = self.camera.y_max/2  

		d = self.camera.distanceToTarget()

		if d > maxDist:
			s = self.WHEEL_PWM_MAX
		else:
			s = int(d/maxDist * self.WHEEL_PWM_MAX)
		
		p = p / 10
		if p > 1 : p = 1
		elif p < -1 : p = -1
		
		self.leftPWM = LEFT_ZERO + s + p

		if self.leftPWM < LEFT_ZERO: self.leftPWM = LEFT_ZERO 
		print("self.letPWM", self.leftPWM, s)
	
	def setRightPWM(self, p):
		maxDist = self.camera.y_max/2  

		d = self.camera.distanceToTarget()

		if d > maxDist:
			s = self.WHEEL_PWM_MAX
		else:
			s = int(d/maxDist * self.WHEEL_PWM_MAX)

		p = p / 10
		if p > 1 : p = 1
		elif p < -1 : p = -1

		self.rightPWM = RIGHT_ZERO - s - p

		if self.rightPWM > RIGHT_ZERO: self.rightPWM = RIGHT_ZERO
		print("self.rightPWM", self.rightPWM, s)




	def updateError(self):
		if self.camera.x == None or self.camera.y == None:
			self.angle = 0
			self.error = 0
		else:	
			self.angle = angle_between(self.camera.p0, self.camera.p1, (self.camera.x, self.camera.y))
			self.error = self.angle * self.camera.distanceToTarget() 

	def updateServos(self):
		pwm.setPWM(RIGHT_WHEEL, 0, int(self.rightPWM))
		pwm.setPWM(LEFT_WHEEL, 0, int(self.leftPWM))

class Camera(object):
	def __init__(self):
		self.pwm_tilt = 630
		self.camera = cv2.VideoCapture(0)

		self.x = None
		self.y = None
		self.radius = None

		# define the lower and upper boundaries of the "green"
		# ball in the HSV color space, then initialize the
		# list of tracked points
		bgr = np.uint8([[[0, 0, 0]]])		#black
		targetColor = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
		diff = (10, 10, 10)
		#diff = (30, 15, 15)		
		self.blackLower = targetColor - diff
		self.blackUpper = targetColor + diff
		self.window = cv2.namedWindow("image")
		cv2.moveWindow("image", 10, 10)

	def distanceToTarget(self):
		if self.x == None or self.y == None:
			return None
		elif self.pwm_tilt == 630:
			return (sqrt(pow(self.p1[0] - self.x, 2) + pow(self.p1[1] - self.y, 2)) - self.radius)/2
		else:
			return sqrt(pow(self.p1[0] - self.x, 2) + pow(self.p1[1] - self.y, 2)) - self.radius

	def setTilt(self):
		window = 20
		if self.x == None or self.y == None:
			
			self.pwm_tilt -= 2
			print "cam angle is ", self.pwm_tilt
			if self.pwm_tilt <= 550:
				self.pwm_tilt = 550
		elif self.y >= self.y_max / 2 + window:
			self.pwm_tilt -= 5
			if self.pwm_tilt < 550:
				self.pwm_tilt = 550
		elif self.y < self.y_max - window:
			self.pwm_tilt += 5
			if self.pwm_tilt > 630:
				self.pwm_tilt = 630
				
		pwm.setPWM(UP_DOWN, 0, self.pwm_tilt)


	def grabFrame(self):
		(grabbed, frame) = self.camera.read()
		# resize the frame, blur it, and convert it to the HSV
		# color space
		frame = imutils.resize(frame, width=600)
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		retval, frame = cv2.threshold(frame, 50, 255, cv2.THRESH_BINARY)
		frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		# construct a mask for the color "green", then perform
		# a series of dilations and erosions to remove any small
		# blobs left in the mask
		mask = cv2.inRange(hsv, self.blackLower, self.blackUpper)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)
	
		# find contours in the mask and initialize the current
		# (x, y) center of the ball
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]

		self.x_max = frame.shape[1]
		self.y_max = frame.shape[0]
		
		self.p0 = (self.x_max / 2, self.y_max)
		self.p1 = (self.x_max / 2, 0)
	
		# "robot"
		cv2.circle(frame, self.p1, 20, (0, 0, 255), -1)
		line = cv2.line(frame, (0, (self.y_max /2 )), (self.x_max, self.y_max/2), (210, 70, 10), 5)
		
			# only proceed if at least one contour was found
		if len(cnts) > 0:
			# find the largest contour in the mask, then use
			# it to compute the minimum enclosing circle and
			# centroid
			c = max(cnts, key=cv2.contourArea)
			((self.x, self.y), self.radius) = cv2.minEnclosingCircle(c)
		
			# only proceed if the radius meets a minimum size
			if self.radius > 10:
			
				# draw the circle and centroid on the frame,
				# then update the list of tracked points
				cv2.circle(frame, (int(self.x), int(self.y)), int(self.radius), (0, 255, 255), 2)
			
				# (x,y) is center of circle
				cv2.circle(frame, (int(self.x),int(self.y)), 5, (0, 255, 0), -1)
				#cv2.circle(frame, p0, 20, (0, 255, 0), -1)
				#angle = angle_between(p0,p1,(x,y))
			else:
				self.x = self.y = self.radiu = None
		
		else:
			self.x = self.y = self.radiu = None

		cv2.imshow("image", frame)

	
	def close(self):
		self.camera.release()
		cv2.destroyAllWindows()


def main():
	camera = Camera()
	robot = Robot(camera)
	pid_params = { 
		"left" :  [.5, -5, 3.32], 
		"right" : [-.5, -5, 3.28]
	}
  
        leftPid = PID(*pid_params['left'])
        rightPid = PID(*pid_params['right'])
        
        # We want to drive the robot towards the 0 angle.
        leftPid.target = 0
        rightPid.target = 0

	start = time()

	while True:
		camera.grabFrame()
		robot.updateError()
		print("error is ", robot.angle, robot.error)

		timestep = time() - start
		print "time step", timestep
 
	        leftAlpha = leftPid(feedback=robot.error, curr_tm=timestep)
        	rightAlpha = rightPid(feedback=robot.error, curr_tm=timestep)
        

		camera.setTilt()
		#robot.setLeftPWM(0)
		#robot.setRightPWM(0)
		robot.setWheelPWM(leftAlpha, rightAlpha)
		robot.updateServos()
		print "self.leftPWM", robot.leftPWM, "self.rightPWM", robot.rightPWM, "leftAlpha", leftAlpha, "rightAlpha", rightAlpha
		
		key = cv2.waitKey(1) & 0xFF
		# if the 'q' key is pressed, stop the loop
		if key == ord("q"):
			break

	camera.close()

	pwm.setPWM(RIGHT_WHEEL, 0, RIGHT_ZERO)
	pwm.setPWM(LEFT_WHEEL, 0, LEFT_ZERO)

if __name__ == "__main__":
	main()

