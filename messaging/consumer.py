import struct
import time
from messaging.kafka_connection import KafkaConnection

class FrameConsumer:
    def __init__(self, topic: str, group_id: str = "video-consumer-group"):
        self.consumer = KafkaConnection.consumer(topic, group_id)

    def __iter__(self):
        for msg in self.consumer:
            data = msg.value
            ts_ns, = struct.unpack('!Q', data[:8])
            t0 = ts_ns / 1e9
            latency = (time.time() - t0) * 1000
            print(f"[LATENCIA] {latency:.1f} ms")
            yield data[8:]