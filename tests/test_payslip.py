from unittest import TestCase

import pathlib
from src.models.payslip import Payslip
from src.models.payslip_date import PayslipDate
from src.models.payslip_recipient import PayslipRecipient


class TestPayslip(TestCase):
    def setUp(self) -> None:
        self.name = "John Doe"
        self.email = "joh@doe.com"
        self.ws_range = ""
        self.sheet_name = ""
        self.payday = PayslipDate("2020-12")
        self.payslip = Payslip(self.name, self.email, self.ws_range, self.payday)

    def test_get_recipient(self):
        expected = PayslipRecipient(self.name, self.email)
        actual = self.payslip.recipient
        self.assertEquals(expected.name, actual.name)
        self.assertEquals(expected.email, actual.email)

    def test_build_filename(self):
        expected = str(pathlib.Path.cwd() / f"files/2020/12/{self.name}.pdf")
        actual = self.payslip.get_abs_filepath()
        self.assertEquals(expected, actual)
