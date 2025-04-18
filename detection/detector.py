import cv2
import numpy as np
from .strategy import BaseDetector

class CaffeDetector(BaseDetector):
    def __init__(self, prototxt: str, model: str, threshold: float):
        self.net = cv2.dnn.readNetFromCaffe(prototxt, model)
        self.threshold = threshold
        self.classes = ["fondo", "avión", "bicicleta", "pájaro", "barco", "botella",
                       "autobús", "coche", "gato", "silla", "vaca", "mesa", "perro",
                       "caballo", "motocicleta", "persona", "planta en maceta", "oveja",
                       "sofá", "tren", "monitor de TV"]
        self.bbox_colors = np.random.uniform(255, 0, size=(len(self.classes), 4))

    def detect(self, frame: np.ndarray) -> np.ndarray:
        frame_flipped = cv2.flip(frame, 1)
        (h, w) = frame_flipped.shape[:2]
        blob = cv2.dnn.blobFromImage(
            cv2.resize(frame_flipped, (300, 300)),
            0.007843,
            (300, 300),
            127.5
        )
        self.net.setInput(blob)
        output = self.net.forward()

        for i in np.arange(0, output.shape[2]):
            confidence = output[0, 0, i, 2]
            if confidence > self.threshold:
                idx = int(output[0, 0, i, 1])
                box = output[0, 0, i, 3:7] * np.array([w, h, w, h])
                startX, startY, endX, endY = box.astype("int")
                bw, bh = endX - startX, endY - startY
                sf = 0.7
                startX = int(startX + bw * (1 - sf) / 2)
                startY = int(startY + bh * (1 - sf) / 2)
                endX = int(endX - bw * (1 - sf) / 2)
                endY = int(endY - bh * (1 - sf) / 2)

                if startX < endX and startY < endY:
                    label = f"{self.classes[idx]}: {confidence*100:.2f}%"
                    if self.classes[idx] == "botella":
                        region = frame_flipped[startY:endY, startX:endX]
                        blurred = cv2.GaussianBlur(region, (95, 95), 0)
                        frame_flipped[startY:endY, startX:endX] = blurred

                    cv2.rectangle(
                        frame_flipped,
                        (startX, startY),
                        (endX, endY),
                        self.bbox_colors[idx],
                        2
                    )
                    cv2.putText(
                        frame_flipped,
                        label,
                        (startX, startY - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 0, 0),
                        2
                    )

        return frame_flipped