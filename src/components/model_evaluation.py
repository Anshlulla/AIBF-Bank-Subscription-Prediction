import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from src.constants import *
from src.utils.utils import *
from src.logging import logging
from src.entity import ModelEvaluationConfig

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig, params_path=PARAMS_FILE_PATH):
        self.config = config
        self.params = read_yaml(params_path).model_trainer

    def evaluate_model(self):
        try:
            logging.info("Starting model evaluation..")
            test_df = pd.read_csv(self.config.test_dir)
            X_test, y_test = test_df.drop("y", axis=1), test_df["y"]
            model = load_pickle(self.config.model_dir)
            if model:
                y_pred = model.predict(X_test)
            else:
                raise ValueError("Model File Not Found")

            accuracy = accuracy_score(y_test, y_pred)
            f1score = f1_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            metrics = {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1score": f1score,
            }

            save_json(self.config.metrics_file, metrics)
            logging.info("Model Evaluation Completed")
            
            return metrics
        except Exception as e:
            raise e
