from dataclasses import dataclass
from typing import Any, Optional

from src.models.payslip_recipient import PayslipRecipient
from src.models.payslip_date import PayslipDate

@dataclass
class Payslip:
    recipient: PayslipRecipient
    payslip_date: PayslipDate
    ws_range: Any
    filepath: Optional[str] = None

    def set_filepath(self, abs_filepath):
        self.filepath = abs_filepath
