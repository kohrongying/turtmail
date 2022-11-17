import os
import logging
from collections import namedtuple
from datetime import datetime

from src.models.payslip_date import PayslipDate
from src.services.email_service import EmailService
from src.services.excel_service import ExcelService
from src.models.payslip_mailer import PayslipMailer
from src.payslip_wb_service import PayslipWbService
from src.services.logging_service import init_logger
from gooey import Gooey, GooeyParser


def get_payslips(wb, payday: str, search_terms: str):
    payslip_date = PayslipDate(payday)
    return PayslipWbService(wb,
                            payslip_date=payslip_date,
                            search_terms=search_terms.split(";")).get_payslips()


def export_payslips(payslips):
    for payslip in payslips:
        payslip.export_to_pdf()


def export_and_send_payslips(payslips, sender_email, email_credential):
    email_service = EmailService(email_credential)
    for payslip in payslips:
        payslip.export_to_pdf()
        mailer = PayslipMailer(payslip, sender_email=sender_email)
        email_service.send(mailer)


@Gooey(program_name="Send Monthly Payslips",
       tabbed_groups=True,
       navigation="Tabbed")
def get_args():
    parser = GooeyParser()

    main_parser = parser.add_argument_group('General Settings',
                                            description="Please input the necessary fields",
                                            gooey_options={
                                                "columns": 1,
                                            })
    main_parser.add_argument('Filepath',
                             help='Select the excel file containing the payslips',
                             widget='FileChooser',
                             gooey_options=dict(wildcard="Excel (.xlsx)|*.xlsx")
                             )
    main_parser.add_argument('-s', '--send_email',
                             action="store_true",
                             default=False,
                             help='Do you wish to send email now?'
                             )
    main_parser.add_argument("-p", '--Payday',
                             widget="DateChooser",
                             default=datetime.today().strftime("%Y-%m-%d"),
                             help='Which month are you sending payslips for?'
                             )

    admin_parser = parser.add_argument_group('Admin Settings',
                                             description='One time setup. Do not change unless you know what you are doing.',
                                             gooey_options={
                                                 "columns": 1,
                                             })
    admin_parser.add_argument('-e', '--sender_email',
                              widget="Textarea",
                              default=os.getenv('sender_email', 'sender@example.com'),
                              help="Email address of sender")
    admin_parser.add_argument('-t', '--search-terms',
                              widget="Textarea",
                              default=os.getenv('search_terms', 'XX Pte Ltd'),
                              help="List of search terms separated by ';' in which one must be present in every payslip")

    admin_parser.add_argument('-a', '--aws-access-key-id',
                              widget="Textarea",
                              default=os.getenv('aws_access_key_id'),
                              help="AWS IAM User Access Key ID used for SES")

    admin_parser.add_argument('-k', '--aws-secret-access-key',
                              widget="Textarea",
                              default=os.getenv('aws_secret_access_key'),
                              help="AWS IAM User Secret Access Key used for SES")

    return parser.parse_args()


if __name__ == '__main__':

    # Set up
    init_logger()
    args = get_args()

    logging.info(f"Your input: {args}")

    wb = ExcelService().open(args.Filepath)
    payslips = get_payslips(wb, payday=args.Payday, search_terms=args.search_terms)

    if args.send_email:
        EmailCredential = namedtuple("EmailCredential", "aws_access_key_id aws_secret_access_key")
        email_cred = EmailCredential(args.aws_access_key_id, args.aws_secret_access_key)
        export_and_send_payslips(payslips, sender_email=args.sender_email, email_credential=email_cred)
    else:
        export_payslips(payslips)

    ExcelService().close(wb)
