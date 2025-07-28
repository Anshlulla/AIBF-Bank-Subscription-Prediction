import os
import yaml
from ensure import ensure_annotations
from box import ConfigBox
from box.exceptions import BoxValueError
from pathlib import Path
from src.logging import logging
import json
import joblib

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads YAML file and returns its contents
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logging.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    
@ensure_annotations
def create_directories(path_to_dirs: list, verbose=True):
    """
    Creates a list of directories
    """
    for path in path_to_dirs:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logging.info(f"Created Directory at: {path}")