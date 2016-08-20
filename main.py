#!/usr/bin/env python
#
# Project: Video Streaming with Flask
# Author: Log0 <im [dot] ckieric [at] gmail [dot] com>
# Date: 2014/12/21
# Website: http://www.chioka.in/
# Description:
# Modified to support streaming out with webcams, and not just raw JPEGs.
# Most of the code credits to Miguel Grinberg, except that I made a small tweak. Thanks!
# Credits: http://blog.miguelgrinberg.com/post/video-streaming-with-flask
#
# Usage:
# 1. Install Python dependencies: cv2, flask. (wish that pip install works like a charm)
# 2. Run "python main.py".
# 3. Navigate the browser to the local webpage.
from flask import Flask, render_template, Response, request, jsonify
from camera import VideoCamera
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera, c='camera1'):
    k = 0
    params = read_params()
    while True:
        if (k%5 == 0):
            params = read_params()

        params['camera'] = c
        frame = camera.get_frame(params)
        k+=1

        if (k == 1000): k = 0

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


#Video Routes
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed1')
def video_feed1():
    return Response(gen(VideoCamera(), 'camera2'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/params_change', methods=['POST'])
def params_change():
    params = read_params()

    with open('params.txt', 'w') as file:
        name = request.form.get('name', type=str)
        value = request.form.get('value', 130, type=int)
        params[name] = value
        json.dump(params, file)

    return jsonify({})

def read_params():
    params = {}
    with open('params.txt', 'r') as f:
        params = json.load(f)

    return params


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, processes=2)





