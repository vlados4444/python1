# excel_report.py
import openpyxl

def create_excel_report(credit_result, deposit_result, file_name="report.xlsx"):
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "Отчет"

    sheet["A1"] = "Кредит"
    sheet["A2"] = "Ежемесячный платеж"
    sheet["B2"] = f"{credit_result[0]:.2f} руб."
    sheet["A3"] = "Общая сумма выплат"
    sheet["B3"] = f"{credit_result[1]:.2f} руб."

    sheet["A5"] = "Вклад"
    sheet["A6"] = "Общая сумма на счете"
    sheet["B6"] = f"{deposit_result[0]:.2f} руб."
    sheet["A7"] = "Начисленные проценты"
    sheet["B7"] = f"{deposit_result[1]:.2f} руб."

    wb.save(file_name)