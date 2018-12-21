from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import time
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type = int, default = 100, help = "# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type = int, default = -1, help = "Whether or not frames should be displayed")
args = vars(ap.parse_args())

camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))
stream = camera.capture_continuous(rawCapture, format = "bgr", use_video_port = True)


print("[INFO] sampling frames from picamera module..")
time.sleep(2.0)
fps = FPS().start()

for (i,f) in enumerate(stream):
	frame = f.array
	frame = imutils.resize(frame, width = 400)
	
	if args["display"] > 0:
                cv2.imshow("Frame", frame)
                key = cv2.waitKey(1) & 0xFF


	rawCapture.truncate(0)
	fps.update()

	if i == args["num_frames"]:
		break

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destoryAllWindows()
stream.close()
rawCapture.close()
camera.close()

print("[INFO] sampling THREADED frames from picamera..")
vs = PiVideoStream().start()
time.sleep(2.0)
fps = FPS().start()

while fps._numFrames < args["num_frames"]:
        frame = vs.read()
        frame = imutils.resize(frame, width = 400)

	if args["display"] > 0:
                cv2.imshow("Frame", frame)
                key = cv2.waitKey(1) & 0xFF

        fps.update()

fps.stop()

print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destoryAllWindows()
vs.stop()

