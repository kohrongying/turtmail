import pathlib
import logging
import sys

from src.arg_parser import ArgParser
from src.email_service import EmailService
from src.excel_service import ExcelService
from src.payslip_mailer import PayslipMailer
from src.payslip_wb_service import PayslipWbService
from validation_service import is_valid_filepath
from datetime import date

if __name__ == '__main__':
    logging.basicConfig(filename=f'logs/{str(date.today())}.log', level=logging.INFO)

    wb_filepath, to_send_email = ArgParser(sys.argv[1:]).get_args()

    logging.info('Checking if filepath is valid')
    is_valid_filepath(wb_filepath)

    wb = ExcelService.open(wb_filepath)
    payslips = PayslipWbService(wb).get_payslips()
    email_service = EmailService()

    for payslip in payslips:
        name = payslip.recipient.name
        filename = str(pathlib.Path.cwd() / f'files/{name}.pdf')

        payslip.ws_range.ExportAsFixedFormat(0, str(pathlib.Path.cwd() / filename))

        mailer = PayslipMailer(payslip.recipient, "December", "2020", filename)
        if to_send_email:
            email_service.send(mailer)
            logging.info('email sent')
