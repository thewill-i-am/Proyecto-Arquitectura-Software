from abc import ABC, abstractmethod
from enum import Enum
import numpy as np

class BaseDetector(ABC):
    @abstractmethod
    def detect(self, frame: np.ndarray) -> np.ndarray:
        pass

class DetectionStrategyType(Enum):
    CAFFE = 1