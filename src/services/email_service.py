import boto3
from botocore.exceptions import ClientError
from src.models.payslip_mailer import PayslipMailer
import logging


class EmailService:
    CONFIGURATION_SET = "ses-cfgset-prd-payslip-service"
    AWS_REGION = "ap-southeast-1"

    def __init__(self, email_credential):
        self.client = boto3.client("ses",
                                   region_name=self.AWS_REGION,
                                   aws_access_key_id=email_credential.aws_access_key_id,
                                   aws_secret_access_key=email_credential.aws_secret_access_key,
                                   )

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
                f"Email sent to {mailer.get_recipient_email()}! "
                f'Message ID: {response["MessageId"]}'
            )
