import cv2
import numpy as np

fn = 'Circles_3.png'

src = cv2.imread(fn, 1)
img = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
img = cv2.medianBlur(img, 5)
cimg = src.copy()

circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, param2 = 30,minRadius = 0, maxRadius = 0)

cirlces = np.unit16(np.around(circles))
if circles is not None:
	for i in circles[0,:]:
		cv2.circle(cimg, i[0], i[1], i[2], (0, 255, 0), 2)
		cv2.circle(cimg, (i[0], i[1]), 2, (0,0,255),3)

cv2.imshow('dected circle', cimg)
#cv2.waitKey(0)
#cv2.destoryAllWindows()
