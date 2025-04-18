# detection/factory.py
from .detector import CaffeDetector
from .strategy import DetectionStrategyType, BaseDetector
import config

class DetectorFactory:
    @staticmethod
    def get_detector(strategy: DetectionStrategyType) -> BaseDetector:
        if strategy == DetectionStrategyType.CAFFE:
            return CaffeDetector(
                config.Config.PROTOTXT_PATH,
                config.Config.MODEL_PATH,
                config.Config.CONFIDENCE_THRESHOLD
            )
        raise ValueError(f"Unknown strategy {strategy}")