from unittest import TestCase

from src.arg_parser import ArgParser


class TestArgParser(TestCase):
    def test_get_args_with_default(self):
        args = ['sample.xlsx']
        expected = ('sample.xlsx', False)
        actual = ArgParser(args).get_args()
        self.assertEqual(expected, actual)

    def test_get_args_with_send_email(self):
        args = ['sample.xlsx', '--send-email']
        expected = ('sample.xlsx', True)
        actual = ArgParser(args).get_args()
        self.assertEqual(expected, actual)