from src.config.configuration import ConfigurationManager
from src.components.model_trainer import ModelTrainer
from src.logging import logging
import pandas as pd

class ModelTrainerPipeline:
    def __init__(self):
        pass

    def _load_data(self):
        try:
            df = pd.read_csv("artifacts/data_transformation/data/processed_data.csv")
            train_df = pd.read_csv("artifacts/data_transformation/data/train.csv")
            test_df = pd.read_csv("artifacts/data_transformation/data/test.csv")
            return train_df, test_df
        except Exception as e:
            raise e

    def initiate_model_trainer(self):
        train_df, test_df = self._load_data()
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer = ModelTrainer(model_trainer_config)
        model_trainer.train(train_df, test_df)

if __name__ == "__main__":
    x = ModelTrainerPipeline()
    x.initiate_model_trainer()