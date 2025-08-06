from src.logging import logger
from src.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from src.pipeline.data_transformation_pipeline import DataTransformationPipeline
from src.pipeline.model_trainer_pipeline import ModelTrainerPipeline

class Pipeline:
    def __init__(self):
        pass

    def data_ingestion(self):
        STAGE_NAME = "Data Ingestion Stage"
        try:
            logger.info(f"Starting stage: {STAGE_NAME}")
            data_ingestion_pipeline = DataIngestionPipeline()
            data_ingestion_pipeline.initiate_data_ingestion()
            logger.info(f"{STAGE_NAME} completed ------")
        except Exception as e:
            logger.exception(e)
            raise e
    
    def data_transformation(self):
        STAGE_NAME = "Data Transformation Stage"
        try:
            logger.info(f"Starting stage: {STAGE_NAME}")
            data_transformation_pipeline = DataTransformationPipeline()
            data_transformation_pipeline.initiate_data_transformation()
            logger.info(f"{STAGE_NAME} completed ------")
        except Exception as e:
            logger.exception(e)
            raise e
        
    def model_trainer(self):
        STAGE_NAME = "Model Trainer Stage"
        try:
            logger.info(f"Starting stage: {STAGE_NAME}")
            model_trainer_pipeline = ModelTrainerPipeline()
            model_trainer_pipeline.initiate_model_trainer()
            logger.info(f"{STAGE_NAME} completed ------")
        except Exception as e:
            logger.exception(e)
            raise e

    def initiate_pipeline(self):
        self.data_ingestion()
        self.data_transformation()
        self.model_trainer()

        