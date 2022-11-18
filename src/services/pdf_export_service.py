from dataclasses import dataclass
from typing import Any

from src.models.payslip import Payslip
from src.models.payslip_recipient import PayslipRecipient
from src.models.payslip_date import PayslipDate
import pathlib
import logging


class PdfExportService:

    def __init__(self, payslip_date, export_dir) -> None:
        self.payslip_date: PayslipDate = payslip_date
        self.export_dir: str = export_dir

    def export_all(self, payslips: List[Payslip]) -> None:
        for payslip in payslips:
            self.export_to_pdf(payslip)

    def export_to_pdf(self, payslip: Payslip) -> None:
        abs_filepath = self.get_abs_filepath()
        payslip.ws_range.ExportAsFixedFormat(0, str(pathlib.Path.cwd() / abs_filepath))
        logging.info(f"Generated {payslip.recipient.name} payslip at {abs_filepath}")

    def get_abs_filepath(self) -> str:
        export_directory = self._get_or_create_month_directory()
        return str(pathlib.Path.cwd() / f"{export_directory}/{self.payslip.recipient.name}.pdf")

    def _get_or_create_month_directory(self) -> str:
        export_directory = f"{self.export_dir}/export/{self.payslip_date.year}/{self.payslip_date.month}"
        pathlib.Path(export_directory).mkdir(parents=True, exist_ok=True)
        return export_directory
