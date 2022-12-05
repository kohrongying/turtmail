from configparser import ConfigParser
from dataclasses import dataclass, asdict


SECTION_KEY = "user_settings"


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
    if SECTION_KEY not in config:
        return PayslipConfig()
    return PayslipConfig(
        aws_access_key_id=config[SECTION_KEY].get("aws_access_key_id", ""),
        aws_secret_access_key=config[SECTION_KEY].get("aws_secret_access_key", ""),
        search_terms=config[SECTION_KEY].get("search_terms", ""),
        sender_email=config[SECTION_KEY].get("sender_email", ""),
        export_dir=config[SECTION_KEY].get("export_dir", ""),
    )


def save_config(filename: str, payslip_config: PayslipConfig) -> None:
    config = ConfigParser()
    config[SECTION_KEY] = payslip_config.dict()
    with open(filename, 'w') as output_file:
        config.write(output_file)
