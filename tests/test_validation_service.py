from pathlib import Path
from unittest import TestCase

from src.validation_service import validate_filepath
from src.exceptions.invalid_input_file import InvalidInputFileException

current_dir = Path(__file__).parent


class TestValidationService(TestCase):
    def test_is_valid_filepath_return_true_given_valid(self):
        # given
        valid_file = current_dir.joinpath("../sample.xlsx")
        self.assertTrue(validate_filepath(valid_file))

    def test_is_valid_filepath_raise_ex_given_invalid(self):
        # given
        invalid_file = current_dir.joinpath("test.xlsx")
        with self.assertRaises(InvalidInputFileException):
            validate_filepath(invalid_file)
