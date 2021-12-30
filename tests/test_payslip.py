from unittest import TestCase

import pathlib
from src.payslip import Payslip
from src.models.payslip_recipient import PayslipRecipient


class TestPayslip(TestCase):

    def setUp(self) -> None:
        self.name = 'John Doe'
        self.email = "joh@doe.com"
        self.ws_range = ''
        self.sheet_name = ''
        self.payslip = Payslip(self.name, self.email, self.sheet_name, self.ws_range)

    def test_get_recipient(self):
        expected = PayslipRecipient(self.name, self.email)
        actual = self.payslip.recipient
        self.assertEquals(expected.name, actual.name)
        self.assertEquals(expected.email, actual.email)

    def test_build_filename(self):
        expected = str(pathlib.Path.cwd() / f'files/{self.name}.pdf')
        actual = self.payslip.filename
        self.assertEquals(expected, actual)

