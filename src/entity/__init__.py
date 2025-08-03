from dataclasses import dataclass
from pathlib import Path
from src.logging import logging

@dataclass
class DataIngestionConfig:
    root_dir: Path
    data_file: Path
    save_file: Path

@dataclass
class DataTransformationConfig:
    root_dir: Path
    data_file: Path
    save_file: Path
    train_dir: Path
    test_dir: Path