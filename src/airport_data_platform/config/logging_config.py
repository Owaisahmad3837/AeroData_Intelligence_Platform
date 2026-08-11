import logging
from pathlib import Path


def logging_config(stage,dataset):

  make_dir = Path("logs") /stage
  make_dir.mkdir(parents=True, exist_ok=True)
  log_file=make_dir / f"{dataset}.log"

  logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
  )
  