from unittest import TestCase

from src.arg_parser import ArgParser
import datetime


class TestArgParser(TestCase):
    def test_get_args_with_send_email(self):
        args = ["sample.xlsx", "--send-email"]
        expected = ("sample.xlsx", True, datetime.datetime.now().__format__("%Y-%m"))
        actual = ArgParser(args).get_args()
        self.assertEqual(expected, actual)

    def test_get_args_with_default(self):
        args = ["sample.xlsx"]
        expected = ("sample.xlsx", False, datetime.datetime.now().__format__("%Y-%m"))
        actual = ArgParser(args).get_args()
        self.assertEqual(expected, actual)

    def test_get_args_with_payday(self):
        args = ["sample.xlsx", "--payday", "2020-06"]
        expected = ("sample.xlsx", False, "2020-06")
        actual = ArgParser(args).get_args()
        self.assertEqual(expected, actual)
