from datetime import datetime


class PayslipDate:
    def __init__(self, date_string: str) -> None:
        self.datetime_object: datetime = datetime.strptime(date_string, "%Y-%m-%d")
        self.mthNum: str = self.datetime_object.strftime("%m")
        self.mthString: str = self.datetime_object.strftime("%B")
        self.yearString: str = self.datetime_object.strftime("%Y")

    def to_string(self):
        return f"{self.mthString} {self.yearString}"
