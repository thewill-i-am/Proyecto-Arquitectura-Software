from kafka import KafkaConsumer
import cv2
import numpy as np
from flask import Flask, Response, render_template

# Configuración del consumidor Kafka
consumer = KafkaConsumer('video-frames', bootstrap_servers='localhost:9092')

app = Flask(__name__)

def generate_frames():
    for message in consumer:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + message.value + b'\r\n')

@app.route('/')
def video_feed():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
