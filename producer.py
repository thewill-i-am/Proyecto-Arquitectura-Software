import cv2
from kafka import KafkaProducer
import threading
import numpy as np
from queue import Queue

class ObjectDetector:
    def __init__(self, model_path, prototxt_path, confidence_threshold=0.50):
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
        frame = cv2.flip(frame, 1)
        (h, w) = frame.shape[:2]
        frame_blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        self.neural_network.setInput(frame_blob)
        neural_network_output = self.neural_network.forward()

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
                    if self.classes[idx] == "botella":
                        # Si se detecta una botella, aplica desenfoque a la región de la botella
                        bottle_region = frame[startY:endY, startX:endX]
                        cv2.rectangle(frame, (startX, startY), (endX, endY), self.bbox_colors[idx], 2)
                        label = "{}: {}%".format(self.classes[idx], round(confidence * 100, 2))
                        cv2.putText(frame, label, (startX, startY - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

                        blurred_bottle_region = cv2.GaussianBlur(bottle_region, (95, 95), 0)
                        frame[startY:endY, startX:endX] = blurred_bottle_region
                    else:
                        cv2.rectangle(frame, (startX, startY), (endX, endY), self.bbox_colors[idx], 2)
                        label = "{}: {}%".format(self.classes[idx], round(confidence * 100, 2))
                        cv2.putText(frame, label, (startX, startY - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        return frame  # Devuelve el frame con objetos detectados

    def send_to_kafka(self, detected_objects):
        for label, detected_frame in detected_objects:
            _, data = cv2.imencode('.jpeg', detected_frame)
            future = self.producer.send(self.topic, data.tobytes())


class FrameProducer:
    def __init__(self, kafka_server, topic, model_path, prototxt_path):
        self.producer = KafkaProducer(bootstrap_servers=kafka_server)
        self.video_capture = cv2.VideoCapture(0)
        self.topic = topic
        self.capture_thread = None
        self.send_thread = None
        self.detector = ObjectDetector(model_path, prototxt_path)
        self.frame_queue = Queue()

    def capture_frames(self):
        while True:
            ret, frame = self.video_capture.read()
            if not ret:
                break

            # Detección de objetos
            detected_frame = self.detector.detect_objects(frame)

            # Agrega el frame detectado a la cola
            self.frame_queue.put(detected_frame)

    def start(self):
        self.capture_thread = threading.Thread(target=self.capture_frames)
        self.send_thread = threading.Thread(target=self.send_frames)
        self.capture_thread.start()
        self.send_thread.start()

    def send_frames(self):
        while True:
            # Toma un frame de la cola
            detected_frame = self.frame_queue.get()
            _, buffer = cv2.imencode('.jpg', detected_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])

            # Envío del frame con objetos detectados
            self.producer.send(self.topic, value=buffer.tobytes())

    def stop(self):
        if self.capture_thread:
            self.capture_thread.join()
        if self.send_thread:
            self.send_thread.join()

if __name__ == "__main__":
    kafka_server = 'localhost:9092'
    topic = 'video-frames'
    model_path = 'MobileNetSSD_deploy.caffemodel'
    prototxt_path = 'MobileNetSSD_deploy.prototxt.txt'

    frame_producer = FrameProducer(kafka_server, topic, model_path, prototxt_path)
    frame_producer.start()

    try:
        frame_producer.capture_thread.join()
    except KeyboardInterrupt:
        print("Deteniendo el productor...")
        frame_producer.stop()
