import cv2
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "-/Expirment01/000005.jpg", required = True, help = "Path to image")
args = vars(ap.parse_args())

image = cv2.imread("-/Expirement01/000005.jpg", 0)
#output = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

circles = cv2.HoughCirlces(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 100)

if circles is not None:
	cirlces = np.round(circles[0,:]).astype("int")

	for (x, y, r) in cirlces:
		cv2.circle(output, (x,y), r, (0, 255, 0), 4)
		cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

cv2.imshow("output", no.hstack([image, output]))
cv2.waitKey(0) 

