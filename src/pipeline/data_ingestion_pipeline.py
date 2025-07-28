from src.config.configuration import ConfigurationManager
from src.components.data_ingestion import DataIngestion
from src.logging import logging

class DataIngestionPipeline:
    def __init__(self):
        pass

    def initiate_data_ingestion(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(data_ingestion_config)
        df = data_ingestion.read_data()
        data_ingestion.save_data(df)