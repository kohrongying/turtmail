import logging
from datetime import date


filename = f'logs/{str(date.today())}.log'
format = "%(asctime)s | %(levelname)s | %(message)s"

logging.basicConfig(
    filename=filename,
    level=logging.INFO,
    format=format
)

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter(format)
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
