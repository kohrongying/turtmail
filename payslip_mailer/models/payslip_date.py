# -*- coding: utf-8 -*-

from datetime import datetime


class PayslipDate:
    def __init__(self, date_string: str) -> None:
        self.datetime_object: datetime = datetime.strptime(date_string, "%Y-%m-%d")

    @property
    def month(self) -> str:
        return self.datetime_object.strftime("%m")

    @property
    def year(self) -> str:
        return self.datetime_object.strftime("%Y")

    @property
    def calendar_month(self) -> str:
        return self.datetime_object.strftime("%B")

    def to_string(self) -> str:
        return f"{self.calendar_month} {self.year}"
