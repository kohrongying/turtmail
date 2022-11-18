import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.models.payslip import Payslip


class PayslipEmailBuilder:

    def __init__(self, payslip, sender_email) -> None:
        self.payslip: Payslip = payslip
        self.sender_email: str = sender_email

        # Create a multipart/mixed parent container.
        self.msg = MIMEMultipart("mixed")

    def build_subject(self):
        self.msg["Subject"] = f"Payslip for {self.payslip.payslip_date.to_string()}"
        return self

    def build_to_from_emails(self):
        self.msg["From"] = self.sender_email
        self.msg["To"] = self.payslip.recipient.email
        return self

    def build_body(self):
        CHARSET = "UTF-8"
        BODY_TEXT = f"""Hi {self.payslip.recipient.name},\r\n\n
Please refer to attached for {self.payslip.payslip_date.to_string()} payslip.\n\n
This is an automated email. Please do not reply.
"""
        msg_body = MIMEMultipart("alternative")
        textpart = MIMEText(BODY_TEXT.encode(CHARSET), "plain", CHARSET)
        msg_body.attach(textpart)
        self.msg.attach(msg_body)
        return self

    def build_attachment(self):
        filepath = self.payslip.filepath
        attachment = MIMEApplication(open(filepath, "rb").read())
        attachment.add_header("Content-Disposition", "attachment", filename=os.path.basename(filepath))
        self.msg.attach(attachment)
        return self

    def get_result(self) -> str:
        return self.msg.as_string()
