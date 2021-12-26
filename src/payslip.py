from src.payslip_recipient import PayslipRecipient
import pathlib


class Payslip:
    export_directory = 'files'

    def __init__(self, name, email, ws_range) -> None:
        self.recipient = PayslipRecipient(name, email)
        self.ws_range = ws_range

    def export_to_pdf(self) -> None:
        self.ws_range.ExportAsFixedFormat(0, str(pathlib.Path.cwd() / self.get_abs_filepath()))

    def get_abs_filepath(self) -> str:
        return str(pathlib.Path.cwd() / f'{self.export_directory}/{self.recipient.name}.pdf')

    def get_export_directory(self):
        return self.export_directory

    def set_export_directory(self, new_directory):
        self.export_directory = new_directory
        pathlib.Path(new_directory).mkdir(parents=True, exist_ok=True)
