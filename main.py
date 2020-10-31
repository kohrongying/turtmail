import win32com.client
from pywintypes import com_error
import pathlib
import argparse
import os
import sys
import logging
from datetime import date
import string

import ses

alphabet = list(string.ascii_uppercase)


def parse_excel(file_path, to_send_email):
    WB_PATH = str(pathlib.Path.cwd() / file_path)

    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False

    try:
        logging.info(f'Opening filename: {WB_PATH}')
        wb = excel.Workbooks.Open(WB_PATH)

        for sheet in wb.Sheets:
            ws = wb.WorkSheets(sheet.Name)

            # Find out used range for the worksheet
            num_cols = ws.UsedRange.Columns.Count
            max_row = ws.UsedRange.Rows.Count  # eg. 68

            # max_col = alphabet[num_cols-1] # eg. 'L'
            max_col = 'L'
            top_left_cell = 'A1'

            # bottom_right_cell = ws.UsedRange.address.replace('$','').split(':')[-1]
            bottom_right_cell = 'L95'

            # Find two ranges for two payslips
            if ws.UsedRange.Find("XX Pte Ltd") is not None:
                logging.info(f'Worksheet {sheet.Name} belongs to XX')
                row_split = ws.Range(f'A1:A{max_row}').Find("XX").Row  # 39
                logging.info(f'Found split at row {row_split}')
            else:
                print(f'Worksheet {sheet.Name} does not have XX company name')
                sys.exit()

            payslip_ranges = [
                f'{top_left_cell}:{max_col}{row_split - 2}',
                f'A{row_split}:{bottom_right_cell}'
            ]

            for rng in payslip_ranges:
                logging.info(f'Current payslip range is {rng}')
                payslip = ws.Range(rng)
                name = payslip.Range('B3').Value

                print(f'name: {name}, range: {rng}')

                email_address = payslip.Range('B4').Value
                filename = str(pathlib.Path.cwd() / f'files/{name}.pdf')
                payslip.ExportAsFixedFormat(0, str(pathlib.Path.cwd() / filename))
                logging.info(f'created: {filename}')

                if to_send_email:
                    logging.info(f'sending {name}\'s payslip to {email_address}')
                    ses.send_email(name, email_address, filename)
                    logging.info('email sent')

        print('\nAll payslips sent')

    except com_error as e:
        print('Excel failed.')
        print(e)
    finally:
        print('\nClosing excel')
        wb.Close()
        excel.Quit()


# Check if file_path is valid
def is_valid_filepath(file_path):
    file_extension = file_path.split('.')[-1]
    if not os.path.exists(file_path):
        print('File does not exist')
        sys.exit()
    if file_extension != 'xlsx':
        print('File has to be of .xlsx type')
        sys.exit()
    return True


if __name__ == '__main__':
    logging.basicConfig(filename=f'logs/{str(date.today())}.log', level=logging.INFO)
    logging.info('Started')

    # argparse
    parser = argparse.ArgumentParser(description='Job to send out payslips email')
    parser.add_argument('file_path', type=str, help='excel file path')
    parser.add_argument('--send-email',
                        nargs='?',
                        type=bool,
                        const=True,
                        default=False,
                        help='Boolean to send email or not'
                        )

    args = vars(parser.parse_args())
    arg_file_path = args['file_path']
    arg_to_send_email = args['send_email']

    logging.info('Checking if filepath is valid')
    is_valid_filepath(arg_file_path)

    parse_excel(arg_file_path, arg_to_send_email)
