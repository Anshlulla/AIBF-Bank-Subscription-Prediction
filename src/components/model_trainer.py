import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score
from imblearn.over_sampling import SMOTE
from src.utils.utils import *
from src.constants import *
from dataclasses import dataclass
from pathlib import Path
from src.logging import logging
from src.entity import ModelTrainerConfig

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig, params_path=PARAMS_FILE_PATH):
        self.config = config
        self.params = read_yaml(params_path).model_trainer
    
    def _resample_data(self, X_train, y_train):
        smote = SMOTE(random_state=self.params["random_state"])
        X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
        return X_train_resampled, y_train_resampled
    
    def _evaluate_model(self, y_true, y_pred):
        try:
            accuracy = accuracy_score(y_true, y_pred)
            f1score = f1_score(y_true, y_pred)
            precision = precision_score(y_true, y_pred)
            recall = recall_score(y_true, y_pred)
            metrics = {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1score": f1score,
            }
            return metrics
        except Exception as e:
            raise e
    
    def train(self, train_df: pd.DataFrame, test_df: pd.DataFrame):
        X_train, y_train = train_df.drop("y", axis=1), train_df["y"]
        X_test, y_test = test_df.drop("y", axis=1), test_df["y"]

        X_train, y_train = self._resample_data(X_train, y_train)
        model = RandomForestClassifier(n_estimators=self.params["n_estimators"],
                                       random_state=self.params["random_state"],
                                       class_weight=self.params["class_weight"])
        logging.info("Model training started")
        model.fit(X_train, y_train)
        logging.info("Model training completed")
        y_pred = model.predict(X_test)
        metrics = self._evaluate_model(y_test, y_pred)
        logging.info("Evaluated model")
        #print(metrics)

        save_path = Path(self.config.model_save_dir)
        os.makedirs(save_path.parent, exist_ok=True)
        save_pickle(model, save_path)
        