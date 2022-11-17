import os
import logging
from src.models.payslip_date import PayslipDate
from src.services.email_service import EmailService
from src.services.excel_service import ExcelService
from src.models.payslip_mailer import PayslipMailer
from src.payslip_wb_service import PayslipWbService
from src.services.logging_service import init_logger
from gooey import Gooey, GooeyParser


def get_payslips(wb, payday: str):
    def get_env_var():
        terms = [os.getenv('search_terms_1', 'XX Pte Ltd')]
        if os.getenv("search_terms_2") is not None:
            terms.append(os.getenv("search_terms_2"))
        return terms
    payslip_date = PayslipDate(payday)
    search_terms = get_env_var()
    return PayslipWbService(wb,
                            payslip_date=payslip_date,
                            search_terms=search_terms).get_payslips()


def export_payslips(payslips):
    for payslip in payslips:
        payslip.export_to_pdf()


def export_and_send_payslips(payslips):
    email_service = EmailService()
    sender_email = os.getenv('sender_email', 'sender@example.com')
    for payslip in payslips:
        payslip.export_to_pdf()
        mailer = PayslipMailer(payslip, sender_email=sender_email)
        email_service.send(mailer)


@Gooey()
def get_args():
    parser = GooeyParser(description='Job to send out payslips email')
    parser.add_argument('file_path',
                        help='Select Excel File',
                        widget='FileChooser',
                        gooey_options=dict(wildcard="Excel (.xlsx)|*.xlsx")
                        )
    parser.add_argument('-s', '--send_email',
                        action="store_true",
                        help='Do you wish to send email now?'
                        )
    parser.add_argument('payday',
                        widget="DateChooser",
                        help='Payslip for which month?'
                        )
    return parser.parse_args()


if __name__ == '__main__':

    # Set up
    init_logger()
    args = get_args()
    logging.info(f"Reading {args.file_path}")

    wb = ExcelService().open(args.file_path)
    payslips = get_payslips(wb, args.payday)

    if args.send_email:
        # export_and_send_payslips(payslips)
        print('sending email')
    else:
        export_payslips(payslips)

    ExcelService().close(wb)
