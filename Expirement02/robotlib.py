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

RIGHT_ZERO = 402 #below 337 forward, above reverse
LEfT_ZER0 = 402  #below 335 reverse, above forward

pwm = PWM(0X40)
pwm.setPWMFreq(60)
