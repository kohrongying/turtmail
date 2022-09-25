import boto3
from botocore.exceptions import ClientError
from src.models.payslip_mailer import PayslipMailer
import logging


class EmailService:
    CONFIGURATION_SET = "payslip-config"
    AWS_REGION = "ap-southeast-1"
    client = boto3.client("ses", region_name=AWS_REGION)

    def send(self, mailer: PayslipMailer) -> None:
        try:
            response = self.client.send_raw_email(
                Source=mailer.get_sender_email(),
                Destinations=[mailer.get_recipient_email()],
                RawMessage={
                    "Data": mailer.build_message().as_string(),
                },
                ConfigurationSetName=self.CONFIGURATION_SET,
            )
        except ClientError as e:
            logging.error(e.response["Error"]["Message"])
        else:
            logging.info(
                f'Email sent to {mailer.get_recipient_email()}! '
                f'Message ID: {response["MessageId"]}'
            )
