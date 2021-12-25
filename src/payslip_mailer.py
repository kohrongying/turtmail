import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from src.payslip_recipient import PayslipRecipient


class PayslipMailer:

    def __init__(self, recipient: PayslipRecipient, payslip_month: str, payslip_yr: str, filepath: str) -> None:
        self.recipient = recipient
        self.payslip_mth_yr = f'{payslip_month} {payslip_yr}'
        self.filepath = filepath

    def build(self):
        SENDER = "SENDEREMAIL@gmail.com"
        SUBJECT = self.build_subject()
        RECIPIENT = self.recipient.email

        # Create a multipart/mixed parent container.
        msg = MIMEMultipart('mixed')
        msg['Subject'] = SUBJECT
        msg['From'] = SENDER
        msg['To'] = RECIPIENT

        msg_body = self.build_body()
        msg.attach(msg_body)

        attachment = self.build_attachment()
        msg.attach(attachment)
        return msg

    def build_subject(self):
        return f'Payslip for {self.payslip_mth_yr}'

    def build_body(self):
        CHARSET = "UTF-8"
        BODY_TEXT = (self.format_body())
        msg_body = MIMEMultipart('alternative')
        textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
        msg_body.attach(textpart)
        return msg_body

    def format_body(self):
        return f"""Hi {self.recipient.name},\r\n\n'
        f'Please refer to attached for {self.payslip_mth_yr} payslip.\n\n'
        'This is an automated email. Please do not reply.'
        """

    def build_attachment(self):
        ATTACHMENT = self.filepath
        att = MIMEApplication(open(ATTACHMENT, 'rb').read())
        att.add_header('Content-Disposition', 'attachment', filename=os.path.basename(ATTACHMENT))
        return att
