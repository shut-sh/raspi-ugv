import time
import RPi.GPIO as GPIO
from PCA9685 import PCA9685

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set which GPIO pins the drive outputs are connected to
DRIVE_1 = 4
DRIVE_2 = 18
DRIVE_3 = 8
DRIVE_4 = 7

LEFT_MOTOR = 14 #18
RIGHT_MOTOR = 23 #8

PAN_NO = 1
TILT_NO = 0
ANGLE_STEP = 10


class UGV(object):
    
    def __init__(self):
        GPIO.setup(DRIVE_1, GPIO.OUT)
        GPIO.setup(DRIVE_2, GPIO.OUT)
        GPIO.setup(DRIVE_3, GPIO.OUT)
        GPIO.setup(DRIVE_4, GPIO.OUT)
        self.pwm = PCA9685()
        self.pwm.setPWMFreq(50)
        self.pan_angle = 10
        self.tilt_angle = 10

    def close(self):
        GPIO.output(DRIVE_1, GPIO.LOW)
        GPIO.output(DRIVE_2, GPIO.LOW)
        GPIO.output(DRIVE_3, GPIO.LOW)
        GPIO.output(DRIVE_4, GPIO.LOW)
        GPIO.cleanup()
        self.pwm.exit_PCA9685()
        self.set_pan_angle(90)
        self.set_tilt_angle(70)

    def forward_key_up(self):
        GPIO.output(LEFT_MOTOR, GPIO.LOW)
        GPIO.output(RIGHT_MOTOR, GPIO.LOW)
        
    def forward_key_down(self):
        GPIO.output(LEFT_MOTOR, GPIO.HIGH)
        GPIO.output(RIGHT_MOTOR, GPIO.HIGH)

    def left_key_up(self):
        GPIO.output(RIGHT_MOTOR, GPIO.LOW)
        
    def left_key_down(self):
        GPIO.output(LEFT_MOTOR, GPIO.LOW)
        GPIO.output(RIGHT_MOTOR, GPIO.HIGH)

    def right_key_up(self):
        GPIO.output(LEFT_MOTOR, GPIO.LOW)
        
    def right_key_down(self):
        GPIO.output(LEFT_MOTOR, GPIO.HIGH)
        GPIO.output(RIGHT_MOTOR, GPIO.LOW)
    
    def set_pan_angle(self, angle):
        if angle > 170 or angle < 10:
            return
        for i in range(self.pan_angle, angle, 1):
            self.pwm.setRotationAngle(PAN_NO, i)   
            self.pan_angle = i
            time.sleep(0.01)
    
    def set_tilt_angle(self, angle):
        if angle > 70 or angle < 10:
            return
        for i in range(self.tilt_angle, angle, 1):
            self.pwm.setRotationAngle(TILT_NO, i)   
            self.tilt_angle = i
            time.sleep(0.01)
    
    def camera_up(self):
        new_angle = self.tilt_angle + ANGLE_STEP
        self.set_tilt_angle(new_angle)
    
    def camera_down(self):
        new_angle = self.tilt_angle - ANGLE_STEP
        self.set_tilt_angle(new_angle)
    
    def camera_left(self):
        new_angle = self.pan_angle + ANGLE_STEP
        self.set_pan_angle(new_angle)
    
    def camera_right(self):
        new_angle = self.pan_angle - ANGLE_STEP
        self.set_pan_angle(new_angle)