from src.logging import logging
from src.pipeline.pipeline import Pipeline

pipeline = Pipeline()
pipeline.initiate_pipeline()
logging.info("---All Pipelines Completed---")