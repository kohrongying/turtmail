from unittest import TestCase

from src.payslip_date import PayslipDate


class TestPayslipDate(TestCase):
    def setUp(self) -> None:
        self.dateString = "2020-12"
        self.payslip_date = PayslipDate(self.dateString)

    def test_get_month(self):
        expected = "December"
        actual = self.payslip_date.get_month(12)
        self.assertEquals(expected, actual)

    def test_get_year(self):
        expected = "2020"
        actual = self.payslip_date.get_year()
        self.assertEquals(expected, actual)

    def test_to_string(self):
        expected = "December 2020"
        actual = self.payslip_date.to_string()
        self.assertEquals(expected, actual)
