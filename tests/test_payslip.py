import pytest

from payslip_mailer.models.payslip import Payslip
from payslip_mailer.models.payslip_date import PayslipDate
from payslip_mailer.models.payslip_recipient import PayslipRecipient


class TestPayslip:
    def test_set_filepath(self, mock_payslip):
        assert mock_payslip.filepath is None
        mock_payslip.set_filepath("this/is/the/absolute/file/path")
        assert mock_payslip.filepath == "this/is/the/absolute/file/path"

    @pytest.fixture
    def mock_payslip(self):
        name = "John Doe"
        email = "joh@doe.com"
        recipient = PayslipRecipient(name, email)
        ws_range = ""
        payday = PayslipDate("2020-12-01")
        return Payslip(recipient, ws_range, payday)

    @pytest.fixture
    def mock_ws_range(self, mocker):
        return mocker.patch("")
