from src.constants import *
from src.utils.utils import *
from src.entity import DataIngestionConfig
from src.logging import logging
import pandas as pd

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def read_data(self) -> pd.DataFrame:
        try:
            df = pd.read_excel(self.config.data_file)
            logging.info(f"Data read successfully from {self.config.data_file}")
            return df
        except Exception as e:
            logging.error(f"Error reading data from {self.config.data_file}: {e}")
            raise e
    
    def save_data(self, df: pd.DataFrame):
        try:
            os.makedirs(self.config.save_file, exist_ok=True)
            file_path = os.path.join(self.config.save_file, "data.csv")
            df.to_csv(file_path, index=False)
            logging.info(f"Data saved successfully to {file_path}")
        except Exception as e:
            logging.error(f"Error saving data to {self.config.save_file}: {e}")
            raise e