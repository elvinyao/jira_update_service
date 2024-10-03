import logging
from logging.handlers import RotatingFileHandler
import os
from app.config import load_config

config = load_config()


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    os.makedirs(config.log_path, exist_ok=True)
    file_handler = RotatingFileHandler(
        os.path.join(config.log_path, f"{name}.log"),
        maxBytes=config.log_max_size,
        backupCount=config.log_max_days
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger