from dataclasses import dataclass
from typing import Any

from src.models.payslip_recipient import PayslipRecipient
from src.models.payslip_date import PayslipDate
import pathlib
import logging

@dataclass
class Payslip:
    recipient: PayslipRecipient
    payslip_date: PayslipDate
    ws_range: Any

    def export_to_pdf(self) -> None:
        export_directory = self._get_or_create_export_directory()
        abs_filepath = self.get_abs_filepath()
        self.ws_range.ExportAsFixedFormat(0, str(pathlib.Path.cwd() / abs_filepath))
        logging.info(f"Exported {self.recipient.name} payslip to {export_directory}")

    def get_abs_filepath(self) -> str:
        export_directory = self._get_or_create_export_directory()
        return str(pathlib.Path.cwd() / f"{export_directory}/{self.recipient.name}.pdf")

    def _get_or_create_export_directory(self) -> str:
        export_directory = f"files/{self.payslip_date.year}/{self.payslip_date.month}"
        pathlib.Path(export_directory).mkdir(parents=True, exist_ok=True)
        return export_directory
