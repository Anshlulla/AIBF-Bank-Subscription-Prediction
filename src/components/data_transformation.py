import os
import pandas as pd
from src.utils.utils import *
from src.constants import *
from src.entity import DataTransformationConfig
from sklearn.preprocessing import StandardScaler
from src.logging import logging

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def read_data(self) -> pd.DataFrame:
        try:
            df = pd.read_csv(self.config.data_file)
            logging.info(f"Data read successfully from {self.config.data_file}")
            return df
        except Exception as e:
            logging.error(f"Error reading data from {self.config.data_file}: {e}")
            raise e

    def one_hot_encode(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            categorical_cols = df.select_dtypes(include=["object"]).columns[:-1]
            new_df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
            new_df.y = df.y.map({"no": 0, "yes": 1})
            new_df = new_df.astype(int)
            logging.info("One Hot Encoded the categorical columns successfully.")
            return new_df
        except Exception as e:
            logging.info("Error while creating one hot labels")
            raise e

    def normalize_cols(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            scaler = StandardScaler()
            num_cols = df.select_dtypes(include=["int64"]).columns
            new_df = self.one_hot_encode(df)
            new_df[num_cols] = scaler.fit_transform(new_df[num_cols])
            logging.info("Standardized numerical columns successfully.")  
            return new_df
        except Exception as e: 
            logging.info("Error while trying to standardize features")
            raise e
        
    def save_data(self, df: pd.DataFrame):
        try:
            os.makedirs(self.config.save_file, exist_ok=True)
            file_path = os.path.join(self.config.save_file, "processed_data.csv")
            df.to_csv(file_path, index=False)
            logging.info(f"Transformed Data saved successfully to {file_path}")
        except Exception as e:
            logging.error(f"Error saving data to {self.config.save_file}: {e}")
            raise e