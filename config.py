# config.py
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    KAFKA_BOOTSTRAP: str = 'localhost:9092'
    TOPIC_PRODUCER: str = 'video-frames'
    CAMERA_SOURCE: int = 0
    MODEL_PATH: str = 'MobileNetSSD_deploy.caffemodel'
    PROTOTXT_PATH: str = 'MobileNetSSD_deploy.prototxt.txt'
    CONFIDENCE_THRESHOLD: float = 0.5