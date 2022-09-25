from src.exceptions.invalid_input_file import InvalidInputFileException
from pathlib import Path


def validate_filepath(file_path: Path) -> bool:
    if not Path.exists(file_path):
        raise InvalidInputFileException('File does not exist')

    if file_path.suffix != '.xlsx':
        raise InvalidInputFileException('File has to be of .xlsx type')
    return True
