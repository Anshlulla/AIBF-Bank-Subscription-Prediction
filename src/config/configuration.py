from pathlib import Path
from src.constants import *
from src.utils.utils import *
from src.entity import DataIngestionConfig, DataTransformationConfig, ModelTrainerConfig


class ConfigurationManager:
    def __init__(self, config_path=CONFIG_FILE_PATH, params_path=PARAMS_FILE_PATH):
        self.config = read_yaml(config_path)
        self.params = read_yaml(params_path)

        create_directories([self.config.artifacts_root])
    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            data_file=config.data_file,
            save_file=config.save_file
        )

        return data_ingestion_config
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation
        create_directories([config.root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir=Path(config.root_dir),
            data_file=Path(config.data_file),
            save_file=Path(config.save_file),
            train_dir=Path(config.train_dir),
            test_dir=Path(config.test_dir)
        )

        return data_transformation_config
    
    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config_path.model_trainer
        create_directories([config.root_dir])

        model_trainer_config = ModelTrainerConfig(
            root_dir=config.root_dir,
            data_file=config.data_file,
            train_dir=config.train_dir,
            test_dir=config.test_dir,
            model_save_dir=config.model_save_dir,
            smote_save_dir=config.smote_save_dir
        )

        return model_trainer_config