from abc import abstractclassmethod
from .streaming_service import StreamingService
from bdaserviceutils import get_kafka_binder_brokers, get_input_channel
from kafka import KafkaConsumer
from abc import ABC, abstractclassmethod


class SinkService(ABC, StreamingService):
    
    alida_service_mode = "sink"
    
    def __init__(self, parser):
        super().__init__(parser)
        self.consumer = self.get_consumer()

    def run(self):
        for message in self.consumer.read_message():
            self.on_message(message=message)

    @abstractclassmethod
    def on_message(self, message):
        pass
