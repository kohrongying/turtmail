import pytest

from payslip_mailer.helpers.payslip_email_builder import PayslipEmailBuilder
from payslip_mailer.models.payslip import Payslip
from payslip_mailer.models.payslip_date import PayslipDate
from payslip_mailer.models.payslip_recipient import PayslipRecipient


class TestPayslipEmailBuilder:
    def test_build_subject(self, mock_payslip):
        builder = PayslipEmailBuilder(mock_payslip, "sender@example.com").build_subject()
        assert builder.msg["Subject"] == "Payslip for December 2020"

    def test_build_to_from_emails(self, mock_payslip):
        builder = PayslipEmailBuilder(
            mock_payslip, "sender@example.com"
        ).build_to_from_emails()
        assert builder.msg["From"] == "sender@example.com"
        assert builder.msg["To"] == "john@doe.com"

    def test_build_body(self, mock_payslip):
        builder = PayslipEmailBuilder(mock_payslip, "sender@example.com").build_body()
        assert len(builder.msg.get_payload()) == 1

    def test_build_attachment(self, mock_payslip):
        builder = PayslipEmailBuilder(mock_payslip, "sender@example.com").build_attachment()
        assert len(builder.msg.get_payload()) == 1

    def test_build_all(self, mock_payslip):
        builder = (
            PayslipEmailBuilder(mock_payslip, "sender@example.com")
            .build_subject()
            .build_to_from_emails()
            .build_body()
            .build_attachment()
        )
        assert builder.msg["Subject"] == "Payslip for December 2020"
        assert builder.msg["From"] == "sender@example.com"
        assert builder.msg["To"] == "john@doe.com"
        assert len(builder.msg.get_payload()) == 2

    @pytest.fixture
    def mock_payslip(self, tmp_path) -> Payslip:
        name = "John Doe"
        email = "john@doe.com"
        recipient = PayslipRecipient(name, email)
        payday = PayslipDate("2020-12-01")

        d = tmp_path / "somepath"
        d.mkdir()
        tmpfile = tmp_path / "payslip.txt"
        tmpfile.write_text("$100")
        return Payslip(
            recipient=recipient, ws_range=None, payslip_date=payday, filepath=str(tmpfile)
        )
