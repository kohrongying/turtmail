# -*- coding: utf-8 -*-

import logging
from dataclasses import dataclass
from typing import List

from payslip_mailer.models.payslip_raw_email import PayslipRawEmail
from payslip_mailer.services.gui_service import get_program_args
from payslip_mailer.models.payslip import Payslip
from payslip_mailer.models.payslip_date import PayslipDate
from payslip_mailer.services.email_service import EmailService
from payslip_mailer.services.excel_service import ExcelService
from payslip_mailer.payslip_wb_service import PayslipWbService
from payslip_mailer.services.logging_service import init_logger
from payslip_mailer.services.pdf_export_service import PdfExportService


@dataclass
class EmailCredential:
    aws_access_key_id: str
    aws_secret_access_key: str


def get_payslips(wb, payslip_date: PayslipDate, search_terms: str) -> List[Payslip]:
    wb_service = PayslipWbService(
        wb, payslip_date=payslip_date, search_terms=search_terms.split(";")
    )
    return wb_service.get_payslips()


def main():
    init_logger()
    args = get_program_args()
    logging.info(f"Your input: {args}")
    payslip_date = PayslipDate(args.Payday)
    search_terms = args.search_terms
    export_dir = args.export_dir

    wb = ExcelService().open(args.Filepath)
    payslips = get_payslips(wb, payslip_date=payslip_date, search_terms=search_terms)

    export_service = PdfExportService(payslip_date=payslip_date, export_dir=export_dir)
    export_service.export_all(payslips)

    if args.send_email:
        email_service = EmailService(
            email_credential=EmailCredential(
                args.aws_access_key_id, args.aws_secret_access_key
            )
        )
        for payslip in payslips:
            mail = PayslipRawEmail(payslip, sender_email=args.sender_email)
            email_service.send(mail)

    ExcelService().close(wb)
