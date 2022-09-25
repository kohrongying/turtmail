import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from src.models.payslip import Payslip


class PayslipMailer:
    def __init__(self, payslip: Payslip, sender_email="sender@example.com") -> None:
        self.payslip = payslip
        self.recipient = payslip.recipient
        self.payslip_date = payslip.payslip_date
        self.filepath = payslip.get_abs_filepath()
        self.sender_email = sender_email

    def build_message(self):
        # Create a multipart/mixed parent container.
        msg = MIMEMultipart("mixed")

        msg["Subject"] = self.build_subject()
        msg["From"] = self.sender_email
        msg["To"] = self.recipient.email

        msg_body = self.build_body()
        msg.attach(msg_body)

        attachment = self.build_attachment()
        msg.attach(attachment)
        return msg

    def build_subject(self):
        return f"Payslip for {self.payslip_date.to_string()}"

    def build_body(self):
        CHARSET = "UTF-8"
        BODY_TEXT = self.format_body()
        msg_body = MIMEMultipart("alternative")
        textpart = MIMEText(BODY_TEXT.encode(CHARSET), "plain", CHARSET)
        msg_body.attach(textpart)
        return msg_body

    def format_body(self):
        return f"""Hi {self.recipient.name},\r\n\n
Please refer to attached for {self.payslip_date.to_string()} payslip.\n\n
This is an automated email. Please do not reply.
"""

    def build_attachment(self):
        ATTACHMENT = self.filepath
        att = MIMEApplication(open(ATTACHMENT, "rb").read())
        att.add_header(
            "Content-Disposition", "attachment", filename=os.path.basename(ATTACHMENT)
        )
        return att

    def get_recipient_email(self):
        return self.recipient.email

    def get_sender_email(self):
        return self.sender_email