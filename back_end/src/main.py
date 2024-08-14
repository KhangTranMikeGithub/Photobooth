#!/usr/bin/env python3
from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO, send, emit

import cv2
from MainCamera import PythonCamera
# from MainPrinter import print_image
app = Flask(__name__)
app.config['SECRET_KEY'] = "adudu1234"
socketio = SocketIO(app, async_mode ="threading")

camera = PythonCamera(0, False)

done = False
change_filter = False
current_filter = None

@app.route("/hello")
def hello(): 
    return "hello"

def modify_frames(frame):
    # print('hello')
    return frame


def generate_frames(filter_param):
    print(filter_param)
    global done

    
    while not done:
        print("not done")
        camera.__init__(0, filter_param)
        frame_generator = camera.main()
        if (frame_generator != None):
            for frame in frame_generator: 
                if frame is None:
                    message = "done"
                    print("called")
                    socketio.emit('message_to_nodejs', message, namespace="/")
                    done = True
                    break
                else:
                    ret, buffer = cv2.imencode('.jpg', frame)
                    buffer_frame = buffer.tobytes()
                    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + buffer_frame + b'\r\n')
            break
    done = False


@socketio.on('connect')
def handle_connect():
    print('Client connected')


def send_message_to_nodejs(message):
    print('triggered')
    socketio.emit('message_to_nodejs', message, namespace='/')


# @app.route('/print')
# def printPhotoDesign():
#     print("Testing print route")
#     firstPic = request.args.get('firstPic')
#     secondPic = request.args.get('secondPic')
#     first_path = f"../../front_end/src/images/{firstPic}.jpg"
#     second_path = f"../../front_end/src/images/{secondPic}.jpg"

#     print_image(first_path, second_path)
#     return "hello"


@app.route('/video')
def video():
    return Response(generate_frames(False), mimetype='multipart/x-mixed-replace; boundary=frame')

    
@app.route('/capture')
def capture():
    return Response(generate_frames(True), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/video/explode')
# def video1():

#     return Response(generate_frames("explode"), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/video/butterflies')
# def video2():
#     return Response(generate_frames("butterflies"), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/video/heart')
# def video3():
#     return Response(generate_frames("heart"), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    socketio.run(app, debug=True)