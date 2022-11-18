import pytest

from src.models.payslip import Payslip
from src.models.payslip_date import PayslipDate
from src.models.payslip_raw_email import PayslipRawEmail
from src.models.payslip_recipient import PayslipRecipient


class TestPayslipRawEmail:
    def test_get_destination(self, mock_payslip_mailer):
        expected = ["john@doe.com"]
        actual = mock_payslip_mailer.destinations
        assert actual == expected

    def test_get_source(self, mock_payslip_mailer):
        expected = "sender@example.com"
        actual = mock_payslip_mailer.source
        assert actual == expected

    def test_build_subject(self, mock_payslip_mailer):
        expected = "Payslip for December 2020"
        actual = mock_payslip_mailer._build_subject()
        assert actual == expected

    def test_format_body(self, mock_payslip_mailer):
        expected = f"""Hi John Doe,\r\n\n
Please refer to attached for December 2020 payslip.\n\n
This is an automated email. Please do not reply.
"""
        actual = mock_payslip_mailer._format_body()
        assert actual == expected

    @pytest.fixture
    def mock_payslip_mailer(self, mock_payslip) -> PayslipRawEmail:
        return PayslipRawEmail(payslip=mock_payslip, sender_email="sender@example.com")

    @pytest.fixture
    def mock_payslip(self) -> Payslip:
        name = "John Doe"
        email = "john@doe.com"
        recipient = PayslipRecipient(name, email)
        payday = PayslipDate("2020-12-01")
        return Payslip(recipient=recipient, ws_range=None, payslip_date=payday)
