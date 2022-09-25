from src.models.payslip_recipient import PayslipRecipient
from src.models.payslip_date import PayslipDate
import pathlib
import logging


class Payslip:
    def __init__(self, name: str, email: str, ws_range, payslip_date: PayslipDate) -> None:
        self.recipient = PayslipRecipient(name, email)
        self.ws_range = ws_range
        self.payslip_date = payslip_date
        self.export_directory = f"files/{payslip_date.yearString}/{payslip_date.mthNum}"

    def export_to_pdf(self) -> None:
        self.is_export_directory_created()
        abs_filepath = self.get_abs_filepath()
        self.ws_range.ExportAsFixedFormat(0, str(pathlib.Path.cwd() / abs_filepath))
        logging.info(f"Exported {self.recipient.name} payslip to {self.export_directory}")

    def get_abs_filepath(self) -> str:
        return str(pathlib.Path.cwd() / f"{self.export_directory}/{self.recipient.name}.pdf")

    def is_export_directory_created(self):
        pathlib.Path(self.export_directory).mkdir(parents=True, exist_ok=True)
