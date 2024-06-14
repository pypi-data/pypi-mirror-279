from abc import abstractclassmethod
from .streaming_service import StreamingService
from bdaserviceutils import get_kafka_binder_brokers, get_input_channel, get_output_channel
from kafka import KafkaConsumer, KafkaProducer
from abc import ABC, abstractclassmethod
import json


class ProcessorService(ABC, StreamingService):

    alida_service_mode = "processor"
    
    def __init__(self, parser):
        super().__init__(parser)
        self.consumer = self.get_consumer()
        self.producer = self.get_producer()

    def run(self):
        for message in self.consumer.read_message():
            self.on_message(message=message)

    @abstractclassmethod
    def on_message(self, message):
        pass

    def send_message(self, message):
        self.producer.send_message(message)
