########################
## DOES NOT WORk ########
########################



import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(1):

	#read frame from capture
	img = cap.read()

	##############
	#do stuff with circles
	
	im = cv2.imread(img, cv2.IMREAD_GRAYSCALE)

	#step up blob detect params
	params = cv2.SimpleBlobDetector_Params()

	#change thresolds
	params.minThreshold = 10
	params.maxThreshold = 200

	# Filter by Area.
	params.filterByArea = True
	params.minArea = 1500

	# Filter by Circularity
	params.filterByCircularity = True
	params.minCircularity = 0.1

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
	
	
	
	
	#############


	cv2.imshow('show image', img)

#exit condition to leave the loop
	k = cv2.waitKey(30) & oxff

	if k == 27:
		break

cv2.destoryAllWindows()
cv2.release()
