import time
import RPi.GPIO as GPIO
from PCA9685 import PCA9685

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set which GPIO pins the drive outputs are connected to
# DRIVE_1 = 4
# DRIVE_2 = 18
# DRIVE_3 = 8
# DRIVE_4 = 7

LEFT_MOTOR = 14 #18
RIGHT_MOTOR = 23 #8

PAN_NO = 0
TILT_NO = 1
ANGLE_STEP = 5


class UGV(object):
    
    def __init__(self, logger):
        GPIO.setup(LEFT_MOTOR, GPIO.OUT)
        GPIO.setup(RIGHT_MOTOR, GPIO.OUT)
        self.pwm = PCA9685()
        self.pwm.setPWMFreq(50)
        self.pan_angle = 10
        self.tilt_angle = 10
        self.logger = logger

    def close(self):
        GPIO.output(LEFT_MOTOR, GPIO.LOW)
        GPIO.output(RIGHT_MOTOR, GPIO.LOW)
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
        step = 1
        if self.pan_angle > angle:
            step = -1
        for i in range(self.pan_angle, angle, step):
            self.pwm.setRotationAngle(PAN_NO, i)   
            self.pan_angle = i
            time.sleep(0.01)
    
    def set_tilt_angle(self, angle):
        if angle > 70 or angle < 10:
            return
        step = 1
        if self.tilt_angle > angle:
            step = -1
        for i in range(self.tilt_angle, angle, step):
            self.pwm.setRotationAngle(TILT_NO, i)   
            self.tilt_angle = i
            time.sleep(0.01)
    
    def camera_up(self):
        self.logger.debug(f"tilt_angle: {self.tilt_angle}")
        new_angle = self.tilt_angle - ANGLE_STEP
        self.set_tilt_angle(new_angle)
    
    def camera_down(self):
        self.logger.debug(f"tilt_angle: {self.tilt_angle}")
        new_angle = self.tilt_angle + ANGLE_STEP
        self.set_tilt_angle(new_angle)
    
    def camera_left(self):
        self.logger.debug(f"pan_angle: {self.pan_angle}")
        new_angle = self.pan_angle + ANGLE_STEP
        self.set_pan_angle(new_angle)
    
    def camera_right(self):
        self.logger.debug(f"pan_angle: {self.pan_angle}")
        new_angle = self.pan_angle - ANGLE_STEP
        self.set_pan_angle(new_angle)