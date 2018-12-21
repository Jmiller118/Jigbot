from Adafruit_PWM_Servo_Driver import PWM
from picamera import PiCamera
from time import sleep


RIGHT_WHEEL = 1
LEFT_WHEEL = 0

UP_DOWN = 5
LEFT_RIGHT = 4
CENTER_CAMERA = 429
MAX_LEFT = CENTER_CAMERA + 150
MAX_RIGHT = CENTER_CAMERA - 150
FLAT = 450

RIGHT_ZERO = 410 #below 410 forward, above reverse
LEFT_ZERO = 410  #below 410 reverse, above forward

pwm = PWM(0X40)
pwm.setPWMFreq(60)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

#pwm.setPWMFreq(60)                        # Set frequency to 60 Hz


