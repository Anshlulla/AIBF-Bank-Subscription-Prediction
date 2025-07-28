from src.config.configuration import ConfigurationManager
from src.components.data_transformation import DataTransformation
from src.logging import logging

class DataTransformationPipeline:
    def __init__(self):
        pass

    def initiate_data_transformation(self):
        config = ConfigurationManager()
        data_transformation_config = config.get_data_transformation_config()
        data_transformation = DataTransformation(data_transformation_config)
        df = data_transformation.read_data()
        new_df = data_transformation.normalize_cols(df)
        data_transformation.save_data(new_df)

if __name__ == "__main__":
    x = DataTransformationPipeline()
    x.initiate_data_transformation()