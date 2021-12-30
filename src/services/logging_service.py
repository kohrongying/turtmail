import logging
from datetime import date


def init_logger():
    filename = f'logs/{str(date.today())}.log'
    logger_format = "%(asctime)s | %(levelname)s | %(message)s"

    logging.basicConfig(
        filename=filename,
        level=logging.INFO,
        format=logger_format
    )

    # set up logging to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(logger_format)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
