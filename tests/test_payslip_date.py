import pytest
from src.exceptions.invalid_payday_exception import InvalidPayDayException
from src.models.payslip_date import PayslipDate


class TestPayslipDate:
    def test_basic(self):
        payslip_date = PayslipDate("2020-12")
        expected = "December 2020"
        actual = payslip_date.to_string()
        assert actual == expected

    def test_single_digit_mth(self):
        payslip_date = PayslipDate("2020-6")
        expected = "June 2020"
        actual = payslip_date.to_string()
        assert actual == expected

    def test_single_digit_lpad_mth(self):
        payslip_date = PayslipDate("2020-06")
        expected = "June 2020"
        actual = payslip_date.to_string()
        assert actual == expected

    def test_invalid_mth(self):
        with pytest.raises(InvalidPayDayException):
            PayslipDate("2020-13")

    def test_invalid_mth_string(self):
        with pytest.raises(InvalidPayDayException):
            PayslipDate("2020-abc")

    def test_invalid_yr_string(self):
        with pytest.raises(InvalidPayDayException):
            PayslipDate("abc-12")
