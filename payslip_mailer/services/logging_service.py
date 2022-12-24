# -*- coding: utf-8 -*-

import logging
from datetime import date
from pathlib import Path


def init_logger() -> None:
    logs_folder = Path(__file__).resolve().parent.parent.parent / "logs"
    Path(logs_folder).mkdir(parents=True, exist_ok=True)
    filename = f"{logs_folder}/{str(date.today())}.log"

    logger_format = "%(asctime)s | %(levelname)s | %(message)s"

    logging.basicConfig(filename=filename, level=logging.INFO, format=logger_format)

    # set up logging to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(logger_format)
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)
