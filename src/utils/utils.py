import os
import yaml
from ensure import ensure_annotations
from box import ConfigBox
from box.exceptions import BoxValueError
from pathlib import Path
from src.logging import logging
import json
import pickle

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

@ensure_annotations
def save_pickle(model, file_path: Path):
    """
    Save a pickle File
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file:
            pickle.dump(model, file=file)
        logging.info(f"Model saved at file path: {file_path}")
    except Exception as e:
        raise e
    
def load_pickle(file_path: Path):
    """
    Load a pickle File
    """
    try:
        with open(file_path, "rb") as f:
            contents = pickle.load(f)
        return contents
    except Exception as e:
        raise e
    
def save_json(file_path: Path, data: dict):
    """
    Saves a json File
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        raise e
    
def load_json(file_path: Path):
    """
    Load a json File
    """
    try:
        with open(file_path, "r") as f:
            contents = json.load(f)
        return contents
    except Exception as e:
        raise e