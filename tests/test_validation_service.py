from pathlib import Path

import pytest

from src.validation_service import validate_filepath
from src.exceptions.invalid_input_file import InvalidInputFileException

current_dir = Path(__file__).parent


class TestValidationService:
    def test_is_valid_filepath_return_true_given_valid(self):
        # given
        valid_file = current_dir.joinpath("../sample.xlsx")
        assert validate_filepath(valid_file) == True

    def test_is_valid_filepath_raise_ex_given_invalid(self):
        # given
        invalid_file = current_dir.joinpath("test.xlsx")
        with pytest.raises(InvalidInputFileException):
            validate_filepath(invalid_file)
