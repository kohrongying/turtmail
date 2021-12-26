from src.payslip_recipient import PayslipRecipient
import pathlib


class PayslipDate:
    MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    def __init__(self, dateString) -> None:
        self.dateString = dateString
        parts = dateString.split('-')
        self.yearString = parts[0]
        self.mthString = self.get_month(parts[1])

    def get_month(self, mth_index: str):
        month_index = int(mth_index)
        return self.MONTHS[month_index-1]

    def get_year(self):
        return self.yearString

    def to_string(self):
        return f'{self.mthString} {self.yearString}'
