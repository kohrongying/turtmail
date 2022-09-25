import unittest
from unittest import TestCase

from src.models.payslip import Payslip
from src.models.payslip_date import PayslipDate
from src.models.payslip_recipient import PayslipRecipient
from src.models.payslip_mailer import PayslipMailer


class TestPayslipMailer(TestCase):
    def setUp(self) -> None:
        name = "John Doe"
        email = "john@doe.com"
        self.recipient = PayslipRecipient(name, email)
        self.payday = PayslipDate("2020-12")
        self.payslip = Payslip(name=name, email=email, ws_range=None, payslip_date=self.payday)
        self.payslip_mailer = PayslipMailer(
            payslip=self.payslip
        )

    def test_build_subject(self):
        expected = "Payslip for December 2020"
        actual = self.payslip_mailer.build_subject()
        self.assertEqual(expected, actual)

    def test_format_body(self):
        expected = f"""Hi John Doe,\r\n\n
Please refer to attached for December 2020 payslip.\n\n
This is an automated email. Please do not reply.
"""
        actual = self.payslip_mailer.format_body()
        self.assertEqual(expected, actual)

    def test_get_recipient_email(self):
        expected = "john@doe.com"
        actual = self.payslip_mailer.get_recipient_email()
        self.assertEqual(expected, actual)

    def test_get_sender_email(self):
        expected = "sender@example.com"
        actual = self.payslip_mailer.get_sender_email()
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
