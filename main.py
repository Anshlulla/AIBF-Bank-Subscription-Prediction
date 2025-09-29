from src.logging import logger
from src.pipeline.pipeline import Pipeline

if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.initiate_pipeline()
    logger.info("---All Pipelines Completed---")