from picamera2 import Picamera2 as PiCamera
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
import time
import io
from datetime import datetime
import numpy as np
from threading import Condition
import cv2 as cv


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()
    
    def read(self):
        with self.condition:
            self.condition.wait()
            return self.frame


class VideoCamera(object):
    # def __init__(self, flip = False, file_type  = ".jpg", ):
    def __init__(self, file_type  = ".jpg", resolution=(320, 240), framerate=32, **kwargs):
        # self.vs = PiVideoStream(resolution=(1920, 1080), framerate=30).start()
        self.flip = False #flip # Flip frame vertically
        self.file_type = file_type # image type i.e. .jpg
        self.camera = PiCamera()

		# set camera parameters
        self.camera.resolution = resolution
        self.camera.framerate = framerate

		# set optional camera parameters (refer to PiCamera docs)
        for (arg, value) in kwargs.items():
            setattr(self.camera, arg, value)

        self.camera.configure(self.camera.create_video_configuration(main={"size": resolution}))
        self.output = StreamingOutput()
        self.camera.start_recording(JpegEncoder(), FileOutput(self.output))
        time.sleep(2.0)

    def __del__(self):
        self.camera.stop_recording()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.flip_if_needed(self.output.read())
        # ret, jpeg = cv.imencode(self.file_type, frame)
        self.previous_frame = frame
        # return jpeg.tobytes()
        return frame

    # Take a photo, called by camera button
    def take_picture(self, photo_string):
        frame = self.flip_if_needed(self.vs.read())
        # ret, image = cv.imencode(self.file_type, frame)
        today_date = datetime.now().strftime("%m%d%Y-%H%M%S") # get current time
        cv.imwrite(str(photo_string + "_" + today_date + self.file_type), frame)
