import cv2
import numpy as np
from messaging.kafka_connection import KafkaConnection
import config

class FrameProducer:
    def __init__(self):
        self.producer = KafkaConnection.producer()
        self.topic = config.Config.TOPIC_PRODUCER

    def send(self, frame: np.ndarray):
        _, buf = cv2.imencode(
            '.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80]
        )
        self.producer.send(self.topic, buf.tobytes())