import unittest
from unittest import TestCase

from src.exceptions.invalid_payslip_sheet_exception import InvalidPayslipSheetException
from src.payslip_ws_service import PayslipWsService


class TestPayslipWsService(TestCase):

    def setUp(self) -> None:
        self.service = PayslipWsService('', '', 'search')

    def test_get_ranges_from_split_row(self):
        expected = [
            'A1:L37',
            'A39:L95'
        ]
        actual = self.service.get_ranges_from_split_row(39)
        self.assertEqual(expected, actual)

    def test_validate_email_address_return_true_given_valid(self):
        # given
        valid_email = 'test@gmail.com'
        self.assertTrue(self.service.validate_email_address(valid_email))

    def test_validate_email_address_raise_ex_given_invalid(self):
        # given
        invalid_email = 'test@gmail'
        with self.assertRaises(InvalidPayslipSheetException):
            self.service.validate_email_address(invalid_email)


if __name__ == '__main__':
    unittest.main()

