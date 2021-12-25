from typing import List

from src.payslip import Payslip
from src.payslip_ws_service import PayslipWsService


class PayslipWbService:
    payslips: List[Payslip] = []

    def __init__(self, wb) -> None:
        self.wb = wb

    def get_payslips(self):
        for sheet in self.wb.Sheets:
            ws = self.wb.WorkSheets(sheet.Name)
            payslips = PayslipWsService(ws, sheet, "XX Pte Ltd").get_payslips()
        return payslips

