import cv2
import struct
import config
from messaging.kafka_connection import KafkaConnection

class FrameProducer:
    def __init__(self):
        self.producer = KafkaConnection.producer()
        self.topic = config.Config.TOPIC_PRODUCER

    def send(self, frame_with_ts: tuple):
        frame, t0 = frame_with_ts
        _, buf = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        ts_ns = int(t0 * 1e9)
        header = struct.pack('!Q', ts_ns)
        self.producer.send(self.topic, header + buf.tobytes())