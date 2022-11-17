from src.exceptions.invalid_payday_exception import InvalidPayDayException


class PayslipDate:
    MONTHS = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    def __init__(self, date_string: str) -> None:
        self.mthNum: str = ""
        self.mthString: str = ""
        self.yearString: str = ""

        self.parse_datestring(date_string)

    def parse_datestring(self, date_string: str) -> None:
        parts = date_string.split("-")
        self.yearString = self.__get_year(parts[0])
        self.mthString = self.__get_month(parts[1])
        self.mthNum = "{:02d}".format(int(parts[1]))

    def __get_month(self, mth_index: str) -> str:
        try:
            month_index = int(mth_index)
            if month_index > 12:
                raise InvalidPayDayException(f"Invalid Month {mth_index} provided")
            return self.MONTHS[month_index - 1]
        except ValueError as e:
            raise InvalidPayDayException(f"Invalid Month {mth_index} provided")

    def __get_year(self, year_string: str) -> str:
        try:
            int(year_string)
            return year_string
        except ValueError as e:
            raise InvalidPayDayException(f"Invalid year {self.yearString} provided")

    def to_string(self):
        return f"{self.mthString} {self.yearString}"
