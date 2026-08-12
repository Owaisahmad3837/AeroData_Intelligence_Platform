import logging
from pathlib import Path

def logging_config(stage, dataset):

    log_dir = Path("logs") / stage
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / f"{dataset}.log"

    logger = logging.getLogger(dataset)
    logger.setLevel(logging.INFO)

    if not logger.handlers:

        handler = logging.FileHandler(log_file)

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger