from src.payslip_recipient import PayslipRecipient
import pathlib


class Payslip:

    def __init__(self, name, email, sheet_name, ws_range) -> None:
        self.recipient = PayslipRecipient(name, email)
        self.sheet_name = sheet_name
        self.ws_range = ws_range
        self.filename = self.build_filename()

    def export_to_pdf(self) -> None:
        self.ws_range.ExportAsFixedFormat(0, str(pathlib.Path.cwd() / self.filename))

    def build_filename(self) -> str:
        return str(pathlib.Path.cwd() / f'files/{self.recipient.name}.pdf')
