from src.exceptions.invalid_input_file import InvalidInputFileException
import os


def is_valid_filepath(file_path):
    file_extension = file_path.split('.')[-1]
    if not os.path.exists(file_path):
        raise InvalidInputFileException('File does not exist')
    if file_extension != 'xlsx':
        raise InvalidInputFileException('File has to be of .xlsx type')
    return True
