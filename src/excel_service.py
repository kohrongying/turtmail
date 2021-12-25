import win32com.client
from pywintypes import com_error


class ExcelService:
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False

    def open(self, workbook_filepath):
        try:
            wb = self.excel.Workbooks.Open(workbook_filepath)
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
