import boto3
from botocore.exceptions import ClientError

from src.common.constants import AWS_REGION
import logging

from src.models.raw_email import RawEmail


class EmailService:
    CONFIGURATION_SET = "ses-cfgset-prd-payslip-service"

    def __init__(self, email_credential):
        self.client = boto3.client(
            "ses",
            region_name=AWS_REGION,
            aws_access_key_id=email_credential.aws_access_key_id,
            aws_secret_access_key=email_credential.aws_secret_access_key,
        )

    def send(self, mail: RawEmail) -> None:
        try:
            response = self.client.send_raw_email(
                Source=mail.source,
                Destinations=mail.destinations,
                RawMessage=mail.raw_message,
                ConfigurationSetName=self.CONFIGURATION_SET,
            )
        except ClientError as e:
            logging.error(e.response["Error"]["Message"])
        else:
            logging.info(
                f"Email sent to {mail.destinations}! " 
                f"Message ID: {response['MessageId']}"
            )
