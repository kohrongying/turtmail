# -*- coding: utf-8 -*-

from configparser import ConfigParser
from dataclasses import dataclass, asdict

from payslip_mailer.common.constants import CONFIG_FILE_SECTION_KEY


@dataclass
class PayslipConfig:
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    search_terms: str = ""
    sender_email: str = ""
    export_dir: str = ""

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


def load_config(filename: str) -> PayslipConfig:
    config = ConfigParser()
    config.read(filename)
    if CONFIG_FILE_SECTION_KEY not in config:
        return PayslipConfig()
    return PayslipConfig(
        aws_access_key_id=config[CONFIG_FILE_SECTION_KEY].get("aws_access_key_id", ""),
        aws_secret_access_key=config[CONFIG_FILE_SECTION_KEY].get("aws_secret_access_key", ""),
        search_terms=config[CONFIG_FILE_SECTION_KEY].get("search_terms", ""),
        sender_email=config[CONFIG_FILE_SECTION_KEY].get("sender_email", ""),
        export_dir=config[CONFIG_FILE_SECTION_KEY].get("export_dir", ""),
    )


def save_config(filename: str, payslip_config: PayslipConfig) -> None:
    config = ConfigParser()
    config[CONFIG_FILE_SECTION_KEY] = payslip_config.dict()
    with open(filename, "w") as output_file:
        config.write(output_file)
