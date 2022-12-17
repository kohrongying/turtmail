from typing import List

from payslip_mailer.models.payslip import Payslip
from payslip_mailer.models.payslip_date import PayslipDate
from payslip_mailer.payslip_ws_service import PayslipWsService
import logging


class PayslipWbService:
    def __init__(self, wb, payslip_date: PayslipDate, search_terms: List[str]) -> None:
        self.wb = wb
        self.payslip_date = payslip_date
        self.search_terms = search_terms
        self.payslips: List[Payslip] = []

    def get_payslips(self) -> List[Payslip]:
        for sheet in self.wb.Sheets:
            ws = self.wb.WorkSheets(sheet.Name)
            sheet_payslips = PayslipWsService(
                ws, search_terms=self.search_terms, payslip_date=self.payslip_date
            ).get_payslips()
            logging.info(f"Found {len(sheet_payslips)} in {sheet.Name}")
            self.payslips.extend(sheet_payslips)

        logging.info(f"Total payslips: {len(self.payslips)}")
        return self.payslips
