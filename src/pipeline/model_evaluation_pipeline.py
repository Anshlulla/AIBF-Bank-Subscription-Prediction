from src.config.configuration import ConfigurationManager
from src.components.model_evaluation import ModelEvaluation
from src.logging import logging
import pandas as pd

class ModelEvaluationPipeline:
    def __init__(self):
        pass

    def initiate_model_evaluation(self):
        config = ConfigurationManager()
        model_evaluation_config = config.get_model_evaluation_config()
        model_evaluation = ModelEvaluation(model_evaluation_config)
        model_evaluation.evaluate_model()

if __name__ == "__main__":
    x = ModelEvaluationPipeline()
    x.initiate_model_evaluation()