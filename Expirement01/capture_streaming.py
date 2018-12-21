import io
import socket
import struct
import time
import picamera

client_socket = socket.socket()
client_socket.connect(('my_server', 8000))
connection = client_socket.makefile('wb')

camera.vflip = True
camera.hflip = True

try:
	with picamera.PiCamera() as camera:
		camera.resolution = (640, 480)
		camera.framerate = 30
		time.sleep(2)
		start = time.time()
		stream = io.BytesIO()

	for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
		connection.write(struct.pack('L', stream.tell()))
		connection.flush()
		stream.seek(0)
		connection.write(stream.read())
		if time.time() - start > 30:
			break	
		stream.seek(0)
		stream.truncate()
	connection.write(struct.pack('L', 0))
finally:
	connection.close()
	client_socket.close()
