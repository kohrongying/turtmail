from unittest import TestCase

from validation_service import is_valid_filepath
from src.exceptions.invalid_input_file import InvalidInputFileException


class TestValidationService(TestCase):
    def test_is_valid_filepath_return_true_given_valid(self):
        # given
        valid_file = '../sample.xlsx'
        self.assertTrue(is_valid_filepath(valid_file))

    def test_is_valid_filepath_raise_ex_given_invalid(self):
        # given
        invalid_file = 'test.xlsx'
        with self.assertRaises(InvalidInputFileException):
            is_valid_filepath(invalid_file)
