from src.payslip_recipient import PayslipRecipient


class Payslip:
    recipient = None
    sheet_name = None
    ws_range = None

    def __init__(self, name, email, sheet_name, wb_range) -> None:
        self.name = name
        self.email = email
        self.sheet_name = sheet_name
        self.ws_range = wb_range

    def get_recipient(self) -> PayslipRecipient:
        return PayslipRecipient(self.name, self.email)

    def get_ws_range(self):
        return self.ws_range