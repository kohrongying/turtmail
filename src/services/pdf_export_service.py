from typing import List

from src.models.payslip import Payslip
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
        abs_filepath = self.get_abs_filepath(payslip)
        payslip.ws_range.ExportAsFixedFormat(0, abs_filepath)
        payslip.set_filepath(abs_filepath)
        logging.info(f"Generated {payslip.recipient.name} payslip at {abs_filepath}")

    def get_abs_filepath(self, payslip: Payslip) -> str:
        export_directory_with_dt = self._get_or_create_export_directory_with_dt()
        return f"{export_directory_with_dt}/{payslip.recipient.name}.pdf"

    def _get_or_create_export_directory_with_dt(self) -> str:
        export_directory = f"{self.export_dir}/export/{self.payslip_date.year}/{self.payslip_date.month}"
        pathlib.Path(export_directory).mkdir(parents=True, exist_ok=True)
        return export_directory
