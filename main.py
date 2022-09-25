import sys
import os
import logging
from src.arg_parser import ArgParser
from src.models.payslip_date import PayslipDate
from src.services.email_service import EmailService
from src.services.excel_service import ExcelService
from src.models.payslip_mailer import PayslipMailer
from src.payslip_wb_service import PayslipWbService
from src.validation_service import validate_filepath
from src.services.logging_service import init_logger


def is_input_valid():
    validate_filepath(wb_filepath)
    PayslipDate(payday)
    logging.info('Input arguments are valid')


def get_payslips(wb, payday):
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


if __name__ == '__main__':
    # Set up
    init_logger()
    wb_filepath, to_send_email, payday = ArgParser(sys.argv[1:]).get_args()
    is_input_valid()

    wb = ExcelService().open(wb_filepath)
    payslips = get_payslips(wb, payday)

    if to_send_email:
        export_and_send_payslips(payslips)
    else:
        export_payslips(payslips)

    ExcelService().close(wb)
