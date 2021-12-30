import boto3
from botocore.exceptions import ClientError
from src.payslip_mailer import PayslipMailer


class EmailService:
    CONFIGURATION_SET = "payslip-config"
    AWS_REGION = "ap-southeast-1"
    client = boto3.client('ses', region_name=AWS_REGION)

    def send(self, mailer: PayslipMailer) -> None:
        try:
            response = self.client.send_raw_email(
                Source=mailer.get_sender_email(),
                Destinations=[mailer.get_recipient_email()],
                RawMessage={
                    'Data': mailer.build_message().as_string(),
                },
                ConfigurationSetName=self.CONFIGURATION_SET
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print(f'Email sent! Message ID: {response["MessageId"]}')

