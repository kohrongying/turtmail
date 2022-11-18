from src.models.payslip_date import PayslipDate


class TestPayslipDate:
    def test_instance_attributes(self):
        payslip_date = PayslipDate("2020-06-27")
        assert payslip_date.month == "06"
        assert payslip_date.calendar_month == "June"
        assert payslip_date.year == "2020"

    def test_basic(self):
        payslip_date = PayslipDate("2020-12-12")
        expected = "December 2020"
        actual = payslip_date.to_string()
        assert actual == expected
