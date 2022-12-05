import os
from datetime import datetime

from gooey import Gooey, GooeyParser

from config_loader import PayslipConfig, load_config, save_config

config_filename = "config.ini"


def save_admin_settings(args) -> PayslipConfig:
    new_payslip_config = PayslipConfig(
        aws_access_key_id=args.aws_access_key_id,
        aws_secret_access_key=args.aws_secret_access_key,
        sender_email=args.sender_email,
        search_terms=args.search_terms,
        export_dir=args.export_dir
    )
    save_config(config_filename, new_payslip_config)
    return new_payslip_config


@Gooey(program_name="Send Monthly Payslips", tabbed_groups=True, navigation="Tabbed")
def get_program_args():
    payslip_config = load_config(config_filename)

    parser = GooeyParser()

    main_parser = parser.add_argument_group(
        "General Settings",
        description="Please input the necessary fields",
        gooey_options={
            "columns": 1,
        },
    )
    main_parser.add_argument(
        "Filepath",
        help="Select the excel file containing the payslips",
        widget="FileChooser",
        gooey_options=dict(wildcard="Excel (.xlsx)|*.xlsx"),
    )
    main_parser.add_argument(
        "-s",
        "--send_email",
        action="store_true",
        default=False,
        help="Do you wish to send email now?",
    )
    main_parser.add_argument(
        "-p",
        "--Payday",
        widget="DateChooser",
        default=datetime.today().strftime("%Y-%m-%d"),
        help="Which month are you sending payslips for?",
    )

    admin_parser = parser.add_argument_group(
        "Admin Settings",
        description="One time setup. Do not change unless you know what you are doing.",
        gooey_options={
            "columns": 1,
        },
    )
    admin_parser.add_argument(
        "-d",
        "--export_dir",
        widget="Textarea",
        default=payslip_config.export_dir if payslip_config.export_dir else os.path.expanduser("~/Desktop"),
        help="Export location of excel files",
    )
    admin_parser.add_argument(
        "-e",
        "--sender_email",
        widget="Textarea",
        default=payslip_config.sender_email if payslip_config.sender_email else os.getenv("sender_email",
                                                                                          "sender@example.com"),
        help="Email address of sender",
    )
    admin_parser.add_argument(
        "-t",
        "--search-terms",
        widget="Textarea",
        default=payslip_config.search_terms if payslip_config.search_terms else os.getenv("search_terms", "XX Pte Ltd"),
        help="List of search terms separated by ';' in which one must be present in every payslip",
    )

    admin_parser.add_argument(
        "-a",
        "--aws-access-key-id",
        widget="Textarea",
        default=payslip_config.aws_access_key_id if payslip_config.aws_access_key_id else os.getenv(
            "aws_access_key_id"),
        help="AWS IAM User Access Key ID used for SES",
    )

    admin_parser.add_argument(
        "-k",
        "--aws-secret-access-key",
        widget="Textarea",
        default=payslip_config.aws_secret_access_key if payslip_config.aws_secret_access_key else os.getenv(
            "aws_secret_access_key"),
        help="AWS IAM User Secret Access Key used for SES",
    )

    input_args = parser.parse_args()
    save_admin_settings(input_args)
    return input_args
