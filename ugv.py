import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set which GPIO pins the drive outputs are connected to
DRIVE_1 = 4
DRIVE_2 = 18
DRIVE_3 = 8
DRIVE_4 = 7

LEFT_MOTOR = 18
RIGHT_MOTOR = 8


class UGV(object):
    
    def __init__(self):
        GPIO.setup(DRIVE_1, GPIO.OUT)
        GPIO.setup(DRIVE_2, GPIO.OUT)
        GPIO.setup(DRIVE_3, GPIO.OUT)
        GPIO.setup(DRIVE_4, GPIO.OUT)

    def close(self):
        GPIO.output(DRIVE_1, GPIO.LOW)
        GPIO.output(DRIVE_2, GPIO.LOW)
        GPIO.output(DRIVE_3, GPIO.LOW)
        GPIO.output(DRIVE_4, GPIO.LOW)
        GPIO.cleanup()

    def forward_key_down(self):
        GPIO.output(LEFT_MOTOR, GPIO.LOW)
        GPIO.output(RIGHT_MOTOR, GPIO.LOW)
        
    def forward_key_up(self):
        GPIO.output(LEFT_MOTOR, GPIO.HIGH)
        GPIO.output(RIGHT_MOTOR, GPIO.HIGH)

    def left_key_down(self):
        GPIO.output(RIGHT_MOTOR, GPIO.LOW)
        
    def left_key_up(self):
        GPIO.output(LEFT_MOTOR, GPIO.LOW)
        GPIO.output(RIGHT_MOTOR, GPIO.HIGH)

    def right_key_down(self):
        GPIO.output(LEFT_MOTOR, GPIO.LOW)
        
    def right_key_up(self):
        GPIO.output(LEFT_MOTOR, GPIO.HIGH)
        GPIO.output(RIGHT_MOTOR, GPIO.LOW)
        