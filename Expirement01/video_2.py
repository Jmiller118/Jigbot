import cv2

if __name__ == '__main__':
	capture = cv2.VideoCapture(0)

	fourcc = cv2.cv.CV_FOURCC(*'XVID')
	video_writer = cv2.VideoWriter('output.avi', fourcc, 20, (680, 480))
while(1):

     #read frame from capture
     img = cap.read()

     ##############################
     # here do the whole stuff with circles and your actual image
     ##############################

     cv2.imshow('show image', img)

     #exit condition to leave the loop
     k = cv2.waitKey(30) & 0xff
     if k == 27:
          break

cv2.destroyAllWindows()
cap.release()
	while (capture.isOpened()):
		ret, frame = capture.read()
		if ret:
			video_writer.write(frame)
			cv2.imshow('Video Stream', frame)

		else:
			break

	capture.release()
	video_writer.release()
	cv2.destoryAllWindows()
