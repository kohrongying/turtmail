# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class PayslipRecipient:
    name: str
    email: str
