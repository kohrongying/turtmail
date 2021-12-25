import win32com.client
from pywintypes import com_error
import pathlib


class ExcelService:
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False

    def open(self, workbook_filepath):
        try:
            wb_abs_path = str(pathlib.Path.cwd() / workbook_filepath)
            wb = self.excel.Workbooks.Open(wb_abs_path)
            return wb
        except com_error as e:
            print(f'Fail to open {e}')
        finally:
            print('\nClosing excel')
            wb.Close()
            self.excel.Quit()

    def close(self, wb):
        wb.Close()
        self.excel.Quit()
