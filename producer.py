import cv2
import numpy as np
from kafka import KafkaProducer
from kafka.errors import KafkaError

class ObjectDetector:
    def __init__(self, model_path, prototxt_path, confidence_threshold=0.80):
        self.neural_network = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
        self.confidence_threshold = confidence_threshold
        self.classes = ["fondo", "avión", "bicicleta", "pájaro", "barco", "botella",
                       "autobús", "coche", "gato", "silla", "vaca", "mesa", "perro",
                       "caballo", "motocicleta", "persona", "planta en maceta", "oveja",
                       "sofá", "tren", "monitor de TV"]
        self.bbox_colors = np.random.uniform(255, 0, size=(len(self.classes), 4))
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
        self.topic = 'my-topic'

    def detect_objects(self, frame):
        (h, w) = frame.shape[:2]
        frame_blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        self.neural_network.setInput(frame_blob)
        neural_network_output = self.neural_network.forward()

        detected_objects = []

        for i in np.arange(0, neural_network_output.shape[2]):
            confidence = neural_network_output[0, 0, i, 2]

            if confidence > self.confidence_threshold:
                idx = int(neural_network_output[0, 0, i, 1])
                bounding_box = neural_network_output[0, 0, i, 3:7] * np.array([w, h, w, h])
                startX, startY, endX, endY = bounding_box.astype("int")
                box_width = endX - startX
                box_height = endY - startY
                shrink_factor = 0.7

                startX = int(startX + box_width * (1 - shrink_factor) / 2)
                startY = int(startY + box_height * (1 - shrink_factor) / 2)
                endX = int(endX - box_width * (1 - shrink_factor) / 2)
                endY = int(endY - box_height * (1 - shrink_factor) / 2)

                if startY < endY and startX < endX:
                    rounded_percentage = round(confidence * 100 / 10) * 10
                    label = "{}: {}%".format(self.classes[idx], rounded_percentage)
                    cv2.rectangle(frame, (startX, startY), (endX, endY), self.bbox_colors[idx], 2)
                    cv2.putText(frame, label, (startX, startY - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                    detected_objects.append((label, frame.copy()))

        return detected_objects

    def send_to_kafka(self, detected_objects):
        for label, detected_frame in detected_objects:
            _, data = cv2.imencode('.jpeg', detected_frame)
            future = self.producer.send(self.topic, data.tobytes())
            
            try:
                future.get(timeout=10)
            except KafkaError as e:
                print(e)

def main():
    detector = ObjectDetector('MobileNetSSD_deploy.caffemodel', 'MobileNetSSD_deploy.prototxt.txt')

    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)
        detected_objects = detector.detect_objects(frame)
        detector.send_to_kafka(detected_objects)

if __name__ == "__main__":
    main()
