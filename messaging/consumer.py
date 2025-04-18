from messaging.kafka_connection import KafkaConnection

class FrameConsumer:
    def __init__(self, topic: str):
        self.consumer = KafkaConnection.consumer(topic)

    def __iter__(self):
        for msg in self.consumer:
            yield msg.value