import struct
import time
from messaging.kafka_connection import KafkaConnection
from prometheus_metrics import FRAME_LATENCY, PROCESSED_FRAMES, AVG_LATENCY

class FrameConsumer:
    def __init__(self, topic: str, group_id: str = "video-consumer-group"):
        self.consumer = KafkaConnection.consumer(topic, group_id)
        self.processed_frames = 0
        self.total_latency = 0

    def __iter__(self):
        for msg in self.consumer:
            data = msg.value
            ts_ns, = struct.unpack('!Q', data[:8])
            t0 = ts_ns / 1e9
            latency = (time.time() - t0) * 1000
            FRAME_LATENCY.set(latency)

            self.total_latency += latency
            self.processed_frames += 1

            avg_latency = self.total_latency / self.processed_frames

            AVG_LATENCY.set(avg_latency)
            PROCESSED_FRAMES.inc()

            yield data[8:]