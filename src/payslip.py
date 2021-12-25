from src.payslip_recipient import PayslipRecipient


class Payslip:
    recipient = None
    sheet_name = None
    ws_range = None

    def __init__(self, name, email, sheet_name, ws_range) -> None:
        self.recipient = PayslipRecipient(name, email)
        self.sheet_name = sheet_name
        self.ws_range = ws_range

    def get_recipient(self) -> PayslipRecipient:
        return self.recipient

    def get_ws_range(self):
        return self.ws_range
