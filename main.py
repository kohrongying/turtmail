import logging
from dataclasses import dataclass
from typing import List

from src.models.payslip_raw_email import PayslipRawEmail
from src.services.gui_service import get_program_args
from src.models.payslip import Payslip
from src.models.payslip_date import PayslipDate
from src.services.email_service import EmailService
from src.services.excel_service import ExcelService
from src.payslip_wb_service import PayslipWbService
from src.services.logging_service import init_logger


@dataclass
class EmailCredential:
    aws_access_key_id: str
    aws_secret_access_key: str


def get_payslips(wb, payday: str, search_terms: str) -> List[Payslip]:
    payslip_date = PayslipDate(payday)
    return PayslipWbService(wb,
                            payslip_date=payslip_date,
                            search_terms=search_terms.split(";")).get_payslips()


def export_payslips(payslips: List[Payslip]):
    for payslip in payslips:
        payslip.export_to_pdf()


def export_and_send_payslips(payslips: List[Payslip], sender_email: str, email_service):
    for payslip in payslips:
        payslip.export_to_pdf()
        mail = PayslipRawEmail(payslip, sender_email=sender_email)
        email_service.send(mail)


def main():
    # Set up
    init_logger()
    args = get_program_args()

    logging.info(f"Your input: {args}")

    wb = ExcelService().open(args.Filepath)
    payslips = get_payslips(wb, payday=args.Payday, search_terms=args.search_terms)

    if args.send_email:
        email_service = EmailService(
            email_credential=EmailCredential(args.aws_access_key_id, args.aws_secret_access_key)
        )
        export_and_send_payslips(payslips, sender_email=args.sender_email, email_service=email_service)
    else:
        export_payslips(payslips)

    ExcelService().close(wb)


if __name__ == '__main__':
    main()
