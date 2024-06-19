from .generic_service import GenericService
from alidadataset.dataset import load as load_dataset

class StreamingService(GenericService):

    def __init__(self, parser):
        super().__init__(parser)

    def get_consumer(self):
        return load_dataset(name="input_dataset", load_as="streaming_input")
    
    def get_producer(self):
        return load_dataset(name="output_dataset", load_as="streaming_output")
