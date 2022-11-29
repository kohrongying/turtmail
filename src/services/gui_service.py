import os
from datetime import datetime

from gooey import Gooey, GooeyParser


@Gooey(program_name="Send Monthly Payslips", tabbed_groups=True, navigation="Tabbed")
def get_program_args():
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
        default=os.path.expanduser("~/Desktop"),
        help="Export location of excel files",
    )
    admin_parser.add_argument(
        "-e",
        "--sender_email",
        widget="Textarea",
        default=os.getenv("sender_email", "sender@example.com"),
        help="Email address of sender",
    )
    admin_parser.add_argument(
        "-t",
        "--search-terms",
        widget="Textarea",
        default=os.getenv("search_terms", "XX Pte Ltd"),
        help="List of search terms separated by ';' in which one must be present in every payslip",
    )

    admin_parser.add_argument(
        "-a",
        "--aws-access-key-id",
        widget="Textarea",
        default=os.getenv("aws_access_key_id"),
        help="AWS IAM User Access Key ID used for SES",
    )

    admin_parser.add_argument(
        "-k",
        "--aws-secret-access-key",
        widget="Textarea",
        default=os.getenv("aws_secret_access_key"),
        help="AWS IAM User Secret Access Key used for SES",
    )

    return parser.parse_args()
