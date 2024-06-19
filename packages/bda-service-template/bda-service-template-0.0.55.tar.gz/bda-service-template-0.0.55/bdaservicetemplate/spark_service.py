from bdaserviceutils import get_args, get_cmd_arg
from .generic_service import GenericService
from alidaargparser import get_asset_property

try: 
    import pysparkutilities
except ImportError:
    import pip
    pip.main(['install', "pyspark-utilities"])

from pysparkutilities.spark_initializer import spark_initializer
from pysparkutilities import ds_initializer, ModelStorage

class SparkService(GenericService):
    def __init__(self, parser, additional_config=[]):
        super().__init__(parser)
        self._args = get_args()
        print(self._args)

        #additional_config = additional_config.append(('spark.jars.packages', 'io.prestosql:presto-jdbc:350'))
        self.spark = spark_initializer("Test-model", self._args, additional_config=additional_config)

    def get_dataset(self, name="input_dataset"):
        data = ds_initializer.load_dataset(sc=self.spark, name=name, read_all=False)
        return data

    def save_dataset(self, dataset, name="output_dataset"):
        ds_initializer.save_dataset(sc=self.spark,name=name, df=dataset)#, output_dest=self._args['output-dataset'])

    def download_model(self, name='input_model'):
        modelStorage = ModelStorage(spark=self.spark, name=name)
        return modelStorage.load_model()

    def upload_model(self, model, name='output_model'):
        if isinstance(model, str):
            super().upload_model(model, name)
        else:       
            outmod = ModelStorage(spark=self.spark, name=name)
            outmod.save_model(model=model)
            
    def get_input_datasets(self):
        datasets = {}
        for dataset in self.parser.input_datasets:
            datasets[dataset.name] = self.get_dataset(dataset.name)
        return next(iter(datasets.values()))
    