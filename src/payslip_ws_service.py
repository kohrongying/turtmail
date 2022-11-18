from typing import List, Optional

from src.exceptions.invalid_payslip_sheet_exception import InvalidPayslipSheetException
from src.models.payslip import Payslip
import re

from src.models.payslip_recipient import PayslipRecipient


class PayslipWsService:
    # Sheet Row and Column limits
    MAX_COL = "L"
    MAX_ROW = "95"
    TOP_LEFT_CELL = "A1"
    BOTTOM_RIGHT_CELL = "L95"

    def __init__(self, ws, search_terms, payslip_date) -> None:
        self.ws = ws
        self.search_terms = search_terms
        self.payslip_date = payslip_date

        self.search_found = None
        self.payslips: List[Payslip] = []
        # self.MAX_ROW = ws.UsedRange.Rows.Count || 0

    def get_payslips(self) -> List[Payslip]:
        try:
            self.check_search_term_exist()
            row_index = self.split_ws_by_search_term()
            payslip_ranges = self.get_ranges_from_split_row(row_index)
            for ws_range in payslip_ranges:
                payslip = self.get_payslip(ws_range)
                if payslip is not None:
                    self.payslips.append(payslip)
            return self.payslips

        except InvalidPayslipSheetException as e:
            print(e)

    def check_search_term_exist(self) -> bool:
        for search_txt in self.search_terms:
            result = self.ws.UsedRange.Find(search_txt)
            if result is not None:
                self.search_found = search_txt
                return True
        raise InvalidPayslipSheetException(f"Worksheet does not have {self.search_terms}")

    def split_ws_by_search_term(self) -> int:
        first_column = f"A1:A{self.MAX_ROW}"
        row_index = self.ws.Range(first_column).Find(self.search_found).Row  # 39
        return row_index

    def get_ranges_from_split_row(self, row_index) -> List[str]:
        r1_top_left = self.TOP_LEFT_CELL
        r1_bottom_right = f"{self.MAX_COL}{row_index - 2}"

        r2_top_left = f"A{row_index}"
        r2_bottom_right = self.BOTTOM_RIGHT_CELL

        return [f"{r1_top_left}:{r1_bottom_right}", f"{r2_top_left}:{r2_bottom_right}"]

    def get_payslip(self, ws_range: str) -> Optional[Payslip]:
        payslip_range = self.ws.Range(ws_range)
        name = payslip_range.Range("B3").Value
        email_address = payslip_range.Range("B4").Value
        if name and email_address:
            self.validate_email_address(email_address)
            recipient = PayslipRecipient(name=name, email=email_address)
            return Payslip(
                recipient=recipient, ws_range=payslip_range, payslip_date=self.payslip_date
            )
        return None

    @staticmethod
    def validate_email_address(email_address) -> Optional[bool]:
        email_regex = re.compile(
            r"([A-Za-z0-9-]+[.-_])*[A-Za-z0-9-]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        )
        if re.fullmatch(email_regex, email_address):
            return True
        raise InvalidPayslipSheetException(f"Invalid email {email_address}")
