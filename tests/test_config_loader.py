from configparser import ConfigParser
from pathlib import Path
from config_loader import load_config, PayslipConfig, save_config, SECTION_KEY


def test_load_config_return_default_values_when_config_file_does_not_exist():
    payslip_config = load_config("")
    assert payslip_config.search_terms == ""
    assert payslip_config.aws_access_key_id == ""
    assert payslip_config.aws_secret_access_key == ""
    assert payslip_config.sender_email == ""
    assert payslip_config.export_dir == ""


def test_load_config_return_values_when_loading_config_file():
    payslip_config = load_config("config.test.ini")
    assert payslip_config.search_terms == "ABCCompany;DEFCompany"
    assert payslip_config.export_dir == 'C:\\User\\Desktop'
    assert payslip_config.aws_access_key_id == ""
    assert payslip_config.aws_secret_access_key == ""
    assert payslip_config.sender_email == ""


def test_save_config():
    payslip_config = PayslipConfig(
        aws_access_key_id="abc@!2",
        export_dir='C:\\User\\Desktop'
    )
    filename = Path.cwd() / "config-write.test.ini"
    save_config(str(filename), payslip_config)
    config = ConfigParser()
    config.read(str(filename))

    assert config[SECTION_KEY].get("aws_access_key_id") == "abc@!2"
    assert config[SECTION_KEY].get("aws_secret_access_key") == ""
    assert config[SECTION_KEY].get("search_terms") == ""
    assert config[SECTION_KEY].get("sender_email") == ""
    assert config[SECTION_KEY].get("export_dir") == 'C:\\User\\Desktop'

    filename.unlink()