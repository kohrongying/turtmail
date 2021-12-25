import pathlib
import argparse
import logging
from src.email_service import EmailService
from src.excel_service import ExcelService
from src.payslip_mailer import PayslipMailer
from src.payslip_wb_service import PayslipWbService
from validation_service import is_valid_filepath
from datetime import date

if __name__ == '__main__':
    logging.basicConfig(filename=f'logs/{str(date.today())}.log', level=logging.INFO)

    # argparse
    parser = argparse.ArgumentParser(description='Job to send out payslips email')
    parser.add_argument('file_path', type=str, help='excel file path')
    parser.add_argument('--send-email',
                        nargs='?',
                        type=bool,
                        const=True,
                        default=False,
                        help='Boolean to send email or not'
                        )

    args = vars(parser.parse_args())
    arg_file_path = args['file_path']
    arg_to_send_email = args['send_email']

    logging.info('Checking if filepath is valid')
    is_valid_filepath(arg_file_path)

    wb = ExcelService.open(arg_file_path)
    payslips = PayslipWbService(wb).get_payslips()
    email_service = EmailService()

    for payslip in payslips:
        name = payslip.recipient.name
        filename = str(pathlib.Path.cwd() / f'files/{name}.pdf')

        payslip.ws_range.ExportAsFixedFormat(0, str(pathlib.Path.cwd() / filename))

        mailer = PayslipMailer(payslip.recipient, "December", "2020", filename)
        if arg_to_send_email:
            email_service.send(mailer)
            logging.info('email sent')

