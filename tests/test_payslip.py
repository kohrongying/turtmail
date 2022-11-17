import pathlib
import pytest

from src.models.payslip import Payslip
from src.models.payslip_date import PayslipDate
from src.models.payslip_recipient import PayslipRecipient


class TestPayslip:
    def test_get_abs_filepath_and_get_export_dir(self, mock_payslip, mocker):
        with mocker.patch("src.models.payslip.pathlib.Path"):
            expected = str(pathlib.Path.cwd() / f"files/2020/12/John Doe.pdf")
            actual = mock_payslip.get_abs_filepath()
            assert actual == expected

    def test_export_to_pdf(self, mock_payslip, mocker):
        pass

    @pytest.fixture
    def mock_payslip(self):
        name = "John Doe"
        email = "joh@doe.com"
        recipient = PayslipRecipient(name, email)
        ws_range = ""
        payday = PayslipDate("2020-12")
        return Payslip(recipient, ws_range, payday)

    @pytest.fixture
    def mock_ws_range(self, mocker):
        return mocker.patch("")
