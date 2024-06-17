from flask import Flask, render_template, Response, request, send_from_directory
from camera import VideoCamera
from ugv import UGV
import os

app = Flask(__name__)

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.
pi_ugv = UGV()

DEBUG = True
def debug(msg):
    if DEBUG:
        print(msg)

@app.route('/')
def index():
    return render_template('index.html') #you can customze index.html here

def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Take a photo when pressing camera button
@app.route('/picture')
def take_picture():
    pi_camera.take_picture()
    return "None"

@app.route('/my event')
def handle_my_event(req):
    debug(f"my event {req}")
    return "None"

@app.route('/forward-keyup')
def handle_forward_keyup():
    debug("forward-keyup")
    pi_ugv.forward_key_up()
    return "None"

@app.route('/left-keyup')
def handle_left_keyup():
    debug("left-keyup")
    pi_ugv.left_key_up()
    return "None"

@app.route('/right-keyup')
def handle_right_keyup():
    debug("right-keyup")
    pi_ugv.right_key_up()
    return "None"

@app.route('/forward-keydown')
def handle_forward_keydown():
    debug("forward-keydown")
    pi_ugv.forward_key_down()
    return "None"

@app.route('/left-keydown')
def handle_left_keydown():
    debug("left-keydown")
    pi_ugv.left_key_down()
    return "None"

@app.route('/right-keydown')
def handle_right_keydown():
    debug("right-keydown")
    pi_ugv.right_key_down()
    return "None"

@app.route('/camera-up')
def handle_camera_up():
    debug("camera_up")
    pi_ugv.camera_up()
    return "None"

@app.route('/camera-down')
def handle_camera_down():
    debug("camera_down")
    pi_ugv.camera_down()
    return "None"

@app.route('/camera-left')
def handle_camera_left():
    debug("camera_left")
    pi_ugv.camera_left()
    return "None"

@app.route('/camera-right')
def handle_camera_right():
    debug("camera_right")
    pi_ugv.camera_right()
    return "None"


if __name__ == '__main__':
    try:
        print("Starting socketio on 0.0.0.0")
        app.run(host='0.0.0.0', debug=True, use_reloader=False)
    finally:
        pi_ugv.close()