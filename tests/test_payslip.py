import pathlib
import pytest

from src.models.payslip import Payslip
from src.models.payslip_date import PayslipDate


class TestPayslip:
    def test_get_recipient(self, mock_payslip):
        actual = mock_payslip.recipient
        assert actual.name == "John Doe"
        assert actual.email == "joh@doe.com"

    def test_build_filename(self, mock_payslip):
        expected = str(pathlib.Path.cwd() / f"files/2020/12/John Doe.pdf")
        actual = mock_payslip.get_abs_filepath()
        assert actual == expected

    @pytest.fixture
    def mock_payslip(self):
        name = "John Doe"
        email = "joh@doe.com"
        ws_range = ""
        payday = PayslipDate("2020-12")
        return Payslip(name, email, ws_range, payday)
