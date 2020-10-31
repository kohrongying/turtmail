import os
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime

SENDER = "SENDEREMAIL@gmail.com"
CHARSET = "UTF-8"
AWS_REGION = "ap-southeast-1"
client = boto3.client('ses', region_name=AWS_REGION)
CONFIGURATION_SET = "payslip-config"


def send_email(name, to_email, file_path):
    SUBJECT = f'Payslip for {datetime.now().__format__("%B %Y")}'
    RECIPIENT = to_email
    BODY_TEXT = (f'Hi {name},\r\n\n'
                 f'Please refer to attached for {datetime.now().__format__("%B %Y")} payslip.\n\n'
                 'This is an automated email. Please do not reply.'
                 )
    ATTACHMENT = file_path

    # Create a multipart/mixed parent container.
    msg = MIMEMultipart('mixed')
    msg['Subject'] = SUBJECT
    msg['From'] = SENDER
    msg['To'] = RECIPIENT
    msg_body = MIMEMultipart('alternative')
    textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
    msg_body.attach(textpart)
    att = MIMEApplication(open(ATTACHMENT, 'rb').read())
    att.add_header('Content-Disposition', 'attachment', filename=os.path.basename(ATTACHMENT))
    msg.attach(msg_body)
    msg.attach(att)

    try:
        response = client.send_raw_email(
            Source=SENDER,
            Destinations=[RECIPIENT],
            RawMessage={
                'Data': msg.as_string(),
            },
            ConfigurationSetName=CONFIGURATION_SET
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print(f'Email sent! Message ID: {response["MessageId"]}')
