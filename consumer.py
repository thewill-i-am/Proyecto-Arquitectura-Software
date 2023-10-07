import io
from flask import Flask, Response
from kafka import KafkaConsumer
from PIL import Image

class ImageProcessor:
    def __init__(self, width=1000, height=800):
        self.WIDTH = width
        self.HEIGHT = height

    def resize_image(self, image_bytes):
        image = Image.open(io.BytesIO(image_bytes))
        image = image.resize((self.WIDTH, self.HEIGHT), Image.ANTIALIAS)
        resized_image_bytes = io.BytesIO()
        image.save(resized_image_bytes, format="JPEG")
        return resized_image_bytes.getvalue()

class KafkaImageStream:
    def __init__(self, topic, bootstrap_servers):
        self.consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers)
        self.image_processor = ImageProcessor()

    def get_frame(self):
        for message in self.consumer:
            resized_image = self.image_processor.resize_image(message.value)
            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + resized_image + b'\r\n\r\n'
            )

app = Flask(__name__)

@app.route('/')
def index():
    kafka_stream = KafkaImageStream('my-topic', 'localhost:9092')
    return Response(
        kafka_stream.get_frame(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

if __name__ == '__main__':
    app.run()
