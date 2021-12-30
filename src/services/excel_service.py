import win32com.client
from pywintypes import com_error
import pathlib
import logging


class ExcelService:
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False

    def open(self, workbook_filepath):
        try:
            wb_abs_path = str(pathlib.Path.cwd() / workbook_filepath)
            wb = self.excel.Workbooks.Open(wb_abs_path)
            return wb
        except com_error as e:
            logging.error(f'Fail to open {e}')
            self.close(wb)

    def close(self, wb):
        logging.info('Closing Workbook now')
        wb.Close()
        self.excel.Quit()
        logging.info('Excel closed')
