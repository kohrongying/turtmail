import pytest

from payslip_mailer.exceptions.invalid_payslip_sheet_exception import (
    InvalidPayslipSheetException,
)
from payslip_mailer.payslip_ws_service import PayslipWsService


class TestPayslipWsService:
    def test_get_ranges_from_split_row(self, mock_service):
        expected = ["A1:L37", "A39:L95"]
        actual = mock_service.get_ranges_from_split_row(39)
        assert actual == expected, actual

    def test_validate_email_address_return_true_given_valid(self, mock_service):
        valid_email = "test-sim@hotmail.com"
        assert mock_service.validate_email_address(valid_email) is True

    def test_validate_email_address_raise_ex_given_invalid(self, mock_service):
        invalid_email = "test@gmail"
        with pytest.raises(InvalidPayslipSheetException):
            mock_service.validate_email_address(invalid_email)

    @pytest.fixture
    def mock_service(self):
        return PayslipWsService("", "", "search")
