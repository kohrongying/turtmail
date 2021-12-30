import sys
from src.arg_parser import ArgParser
from src.payslip_date import PayslipDate
from src.services.email_service import EmailService
from src.services.excel_service import ExcelService
from src.payslip_mailer import PayslipMailer
from src.payslip_wb_service import PayslipWbService
from validation_service import is_valid_filepath
from src.services.logging_service import init_logger
import logging


if __name__ == '__main__':
    init_logger()

    wb_filepath, to_send_email, payday = ArgParser(sys.argv[1:]).get_args()

    is_valid_filepath(wb_filepath)
    payslip_date = PayslipDate(payday)
    logging.info('Input arguments are valid')

    wb = ExcelService().open(wb_filepath)
    payslips = PayslipWbService(wb).get_payslips()
    email_service = EmailService()
    for payslip in payslips:
        payslip.set_export_directory(f'files/{payslip_date.yearString}/{payslip_date.mthNum}')
        payslip.export_to_pdf()

        if to_send_email:
            mailer = PayslipMailer(payslip.recipient, payslip_date, payslip.get_abs_filepath())
            email_service.send(mailer)

    ExcelService().close(wb)
