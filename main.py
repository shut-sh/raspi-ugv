from flask import Flask, render_template, Response, request, send_from_directory
from camera import VideoCamera
from ugv import UGV
import os
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mylittlesecret!'
socketio = SocketIO(app, debug=True, cors_allowed_origins='*', async_mode='eventlet')

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.
pi_ugv = UGV()

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

@socketio.on('my event')
def handle_my_event(req):
    print(f"my event {req}")

@socketio.on('forward-keyup')
def handle_forward_keyup():
    print("forward-keyup")
    pi_ugv.forward_key_up()

@socketio.on('left-keyup')
def handle_left_keyup():
    print("left-keyup")
    pi_ugv.left_key_up()

@socketio.on('right-keyup')
def handle_right_keyup():
    print("right-keyup")
    pi_ugv.right_key_up()

@socketio.on('forward-keydown')
def handle_forward_keydown():
    print("forward-keydown")
    pi_ugv.forward_key_down()

@socketio.on('left-keydown')
def handle_left_keydown():
    print("left-keydown")
    pi_ugv.left_key_down()

@socketio.on('right-keydown')
def handle_forward_keydown():
    print("right-keydown")
    pi_ugv.forward_key_down()


if __name__ == '__main__':
    try:
        socketio.run(app, host='0.0.0.0', debug=False)
    finally:
        pi_ugv.close()