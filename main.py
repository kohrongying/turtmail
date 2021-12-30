import sys
from src.arg_parser import ArgParser
from src.models.payslip_date import PayslipDate
from src.services.email_service import EmailService
from src.services.excel_service import ExcelService
from src.payslip_mailer import PayslipMailer
from src.payslip_wb_service import PayslipWbService
from validation_service import is_valid_filepath
from src.services.logging_service import init_logger
import logging


def is_input_valid():
    is_valid_filepath(wb_filepath)
    PayslipDate(payday)
    logging.info('Input arguments are valid')


def get_payslips(wb, payday):
    payslip_date = PayslipDate(payday)
    search_terms = ['XX Pte Ltd']
    return PayslipWbService(wb,
                            payslip_date=payslip_date,
                            search_terms=search_terms).get_payslips()


def export_payslips(payslips):
    for payslip in payslips:
        payslip.export_to_pdf()


def export_and_send_payslips(payslips):
    email_service = EmailService()
    sender_email = 'sender@example.com'
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
