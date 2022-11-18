import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Dict

from src.models.payslip import Payslip
from src.models.raw_email import RawEmail


class PayslipRawEmail(RawEmail):
    def __init__(self, payslip, sender_email):
        self.payslip: Payslip = payslip
        self.sender_email: str = sender_email

    @property
    def source(self) -> str:
        return self.sender_email

    @property
    def destinations(self) -> List[str]:
        return [self.payslip.recipient.email]

    @property
    def raw_message(self) -> Dict[str, str]:
        return {"Data": self._build_raw_message().as_string()}

    def _build_raw_message(self) -> MIMEMultipart:
        # Create a multipart/mixed parent container.
        msg = MIMEMultipart("mixed")

        msg["Subject"] = self._build_subject()
        msg["From"] = self.sender_email
        msg["To"] = self.payslip.recipient.email

        msg_body = self._build_body()
        msg.attach(msg_body)

        attachment = self._build_attachment()
        msg.attach(attachment)
        return msg

    def _build_subject(self):
        return f"Payslip for {self.payslip.payslip_date.to_string()}"

    def _build_body(self):
        CHARSET = "UTF-8"
        BODY_TEXT = self._format_body()
        msg_body = MIMEMultipart("alternative")
        textpart = MIMEText(BODY_TEXT.encode(CHARSET), "plain", CHARSET)
        msg_body.attach(textpart)
        return msg_body

    def _format_body(self):
        return f"""Hi {self.payslip.recipient.name},\r\n\n
Please refer to attached for {self.payslip.payslip_date.to_string()} payslip.\n\n
This is an automated email. Please do not reply.
"""

    def _build_attachment(self):
        ATTACHMENT = self.payslip.get_abs_filepath()
        att = MIMEApplication(open(ATTACHMENT, "rb").read())
        att.add_header(
            "Content-Disposition", "attachment", filename=os.path.basename(ATTACHMENT)
        )
        return att
