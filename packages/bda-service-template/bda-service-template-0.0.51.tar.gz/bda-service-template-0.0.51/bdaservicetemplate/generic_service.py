import os
import logging
from bdaserviceutils import get_args
from dsioutilities import Dataset
from .utils import packages_are_installed
from alidaargparser.assets_utils import get_asset_properties

if packages_are_installed(['fileioutilities']):
    from fileioutilities.file_io import FileIO
else:
    logging.warning("Please install fileioutilities (https://pypi.org/project/file-io-utilities) if you want to use models in your service.")

class GenericService():
    def __init__(self, parser):
        super().__init__()
        
        # Raw args
        self._args = get_args()
        
        self.parser = parser
        
        # Parsed args
        self.args = self.parser.parse_args()
        
        # Set ports to expose
        self.ports = self.parser.parse_ports()

        # If only one port is present, set it as self.port
        if len(self.ports.values())==1:
            self.port = list(self.ports.values())[0]

    def get_assets_info(self):
        
        info = {"datasets": {}, "models": {}}

        for dataset in self.parser.input_datasets:
            props = get_asset_properties(dataset.name)
            info['datasets'][dataset.name] = props

        for dataset in self.parser.output_datasets:
            props = get_asset_properties(dataset.name)
            info['datasets'][dataset.name] = props

        for model in self.parser.input_models:
            props = get_asset_properties(model.name)
            info['models'][model.name] = props

        for model in self.parser.output_models:
            props = get_asset_properties(model.name)
            info['models'][model.name] = props


        return info

    def get_datasets_full(self):
        datasets = {}
        for dataset in self.parser.input_datasets:
            datasets[dataset.name] = self.get_dataset(dataset.name)
        return datasets

    def get_input_datasets(self):
        datasets = {}
        for dataset in self.parser.input_datasets:
            datasets[dataset.name] = self.get_dataset(dataset.name)
        return datasets
    
    def get_output_datasets(self):
        datasets = {}
        for dataset in self.parser.output_datasets:
            datasets[dataset.name] = self.get_dataset(dataset.name)
        return datasets


    def get_datasets(self):
        datasets = self.get_datasets_full()

        # If only one dataset, return it directly
        if len(datasets) == 1:
            return datasets[next(iter(datasets))]

        return datasets

    def save_datasets(self, datasets):
        if isinstance(datasets, dict):
            for dataset in self.parser.output_datasets:
                self.save_dataset(datasets[dataset.name], dataset.name)
        # If only one dataset a dictionary is not expected
        else:
            self.save_dataset(datasets, self.parser.output_datasets[0].name)


    def get_models_full(self):
        models = {}
        for model in self.parser.input_models:
            models[model.name] = self.download_model(model.name)

        return models


    def download_models(self):
        models = self.get_models_full()
        
        # If only one model, return it directly
        if len(models) == 1:
            return models[next(iter(models))]
        
        return models

    def upload_models(self, models):     
        if isinstance(models, dict):
            for model in self.parser.output_models:
                self.upload_model(models[model.name], model.name)   
        # If only one dataset a dictionary is not expected
        else:
            self.upload_model(models, self.parser.output_models[0].name)

    def get_dataset(self, name="input-dataset"):
        return Dataset(name, dataset_type="object")

    def get_output_dataset(self, name="output-dataset"):
        return self.get_dataset(name)

    def save_dataset(self, dataset, name="output-dataset"):
        pass

    def download_model(self, name='input_model'):
        path = os.path.join(".", "model")
        FileIO(name=name).download(local_path=path)
        return path

    def upload_model(self, path, name='output_model'):
        fileIO = FileIO(name=name)
        fileIO.upload(local_path=path)
