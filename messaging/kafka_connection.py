from kafka import KafkaProducer, KafkaConsumer
import config

class KafkaConnection:
    _producer = None

    @classmethod
    def producer(cls) -> KafkaProducer:
        if cls._producer is None:
            cls._producer = KafkaProducer(
                bootstrap_servers=config.Config.KAFKA_BOOTSTRAP
            )
        return cls._producer

    @classmethod
    def consumer(cls, topic: str, group_id: str = None) -> KafkaConsumer:
        return KafkaConsumer(
            topic,
            bootstrap_servers=config.Config.KAFKA_BOOTSTRAP,
            group_id=group_id,
            auto_offset_reset='latest',
            enable_auto_commit=True,
            consumer_timeout_ms=1000
        )
