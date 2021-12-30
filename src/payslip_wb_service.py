from typing import List

from src.payslip import Payslip
from src.payslip_ws_service import PayslipWsService
import logging


class PayslipWbService:
    payslips: List[Payslip] = []

    def __init__(self, wb) -> None:
        self.wb = wb

    def get_payslips(self) -> List[Payslip]:
        search_terms = ['XX Pte Ltd']
        for sheet in self.wb.Sheets:
            ws = self.wb.WorkSheets(sheet.Name)
            if self.is_valid_sheet(sheet):
                sheet_payslips = PayslipWsService(ws, sheet, search_terms).get_payslips()
                logging.info(f'Found {len(sheet_payslips)} in {sheet.Name}')
                self.payslips.extend(sheet_payslips)

        logging.info(f'payslips: {len(self.payslips)}')
        return self.payslips

    def is_valid_sheet(self, sheet):
        return '&' in sheet.Name

