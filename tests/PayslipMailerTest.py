import unittest
from src.payslip_recipient import PayslipRecipient
from src.payslip_mailer import PayslipMailer


class PayslipMailerTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.recipient = PayslipRecipient("John Doe", "john@doe.com")
        self.payslip_mailer = PayslipMailer(recipient=self.recipient,
                                            payslip_month="December",
                                            payslip_yr="2020",
                                            filepath="./test.pdf")

    def test_build_subject(self):
        expected = 'Payslip for December 2020'
        actual = self.payslip_mailer.build_subject()
        self.assertEqual(expected, actual)

    def test_format_body(self):
        expected = f"""Hi John Doe,\r\n\n'
        f'Please refer to attached for December 2020 payslip.\n\n'
        'This is an automated email. Please do not reply.'
        """
        actual = self.payslip_mailer.format_body()
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
