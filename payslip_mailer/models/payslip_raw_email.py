from typing import List, Dict

from payslip_mailer.helpers.payslip_email_builder import PayslipEmailBuilder
from payslip_mailer.models.payslip import Payslip
from payslip_mailer.models.raw_email import RawEmail


class PayslipRawEmail(RawEmail):
    def __init__(self, payslip, sender_email):
        self.payslip: Payslip = payslip
        self.sender_email: str = sender_email

    @property
    def source(self) -> str:
        return self.sender_email

    @property
    def destinations(self) -> List[str]:
        return [self.payslip.recipient.email]

    @property
    def raw_message(self) -> Dict[str, str]:
        builder = (
            PayslipEmailBuilder(self.payslip, self.sender_email)
            .build_subject()
            .build_to_from_emails()
            .build_body()
            .build_attachment()
        )
        return {"Data": builder.get_result()}
