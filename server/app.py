import time
from flask import Flask
import threading
import cv2
import config
from buffering.frame_buffer import FrameBuffer
from detection.factory import DetectorFactory
from detection.strategy import DetectionStrategyType
from messaging.producer import FrameProducer
from messaging.consumer import FrameConsumer
from server.routes import VideoRoutes
from prometheus_metrics import FRAME_LATENCY, BUFFER_SIZE, PROCESSED_FRAMES, AVG_LATENCY, CAPTURE_FPS


app = Flask(__name__)
buffer = FrameBuffer()

def capture_loop():
    cap = cv2.VideoCapture(config.Config.CAMERA_SOURCE)
    detector = DetectorFactory.get_detector(DetectionStrategyType.CAFFE)
    frame_count = 0
    start_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        t0 = time.time()
        processed = detector.detect(frame)
        buffer.put((processed, t0))

        if frame_count % 100 == 0:
            elapsed_time = time.time() - start_time
            fps = frame_count / elapsed_time
            CAPTURE_FPS.set(fps)

threading.Thread(target=capture_loop, daemon=True).start()

producer = FrameProducer()

def send_loop():
    while True:
        item = buffer.get()
        buffer_size = buffer.queue.qsize()
        BUFFER_SIZE.set(buffer_size)
        producer.send(item)

threading.Thread(target=send_loop, daemon=True).start()

@app.route('/')
def index():
    return VideoRoutes.video_feed()

@app.route('/video')
def video():
    consumer = FrameConsumer(config.Config.TOPIC_PRODUCER)
    def gen():
        for buf in consumer:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buf + b'\r\n')
    return VideoRoutes.video_stream(gen())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, threaded=True)