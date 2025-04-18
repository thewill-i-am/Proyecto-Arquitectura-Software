from kafka import KafkaProducer, KafkaConsumer
import config

class KafkaConnection:
    _producer = None
    _consumer = None

    @classmethod
    def producer(cls) -> KafkaProducer:
        if cls._producer is None:
            cls._producer = KafkaProducer(
                bootstrap_servers=config.Config.KAFKA_BOOTSTRAP
            )
        return cls._producer

    @classmethod
    def consumer(cls, topic: str) -> KafkaConsumer:
        if cls._consumer is None:
            cls._consumer = KafkaConsumer(
                topic,
                bootstrap_servers=config.Config.KAFKA_BOOTSTRAP
            )
        return cls._consumer