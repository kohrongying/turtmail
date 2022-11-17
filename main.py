import os
import logging
from datetime import datetime

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


@Gooey(program_name="Send Monthly Payslips")
def get_args():
    parser = GooeyParser()
    parser.add_argument('Filepath',
                        help='Select the excel file containing the payslips',
                        widget='FileChooser',
                        gooey_options=dict(wildcard="Excel (.xlsx)|*.xlsx")
                        )
    parser.add_argument('-s', '--send_email',
                        action="store_true",
                        default=False,
                        help='Do you wish to send email now?'
                        )
    parser.add_argument("-p", '--Payday',
                        widget="DateChooser",
                        default=datetime.today().strftime("%Y-%m-%d"),
                        help='Which month are you sending payslips for?'
                        )
    return parser.parse_args()


if __name__ == '__main__':

    # Set up
    init_logger()
    args = get_args()

    logging.info(f"Your input: {args}")

    wb = ExcelService().open(args.Filepath)
    payslips = get_payslips(wb, args.Payday)

    if args.send_email:
        # export_and_send_payslips(payslips)
        print('sending email')
    else:
        export_payslips(payslips)

    ExcelService().close(wb)
