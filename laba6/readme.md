# Лабораторная работа 6
 Задание 
 Банковские услуги

    Кредит
    Рассрочка
    Вклад

Расчёт процентов, графика платежей.

Фреймворк PySimpleGUI

Код по bank services

~~~python
import PySimpleGUI as sg
from bank_services import calculate_credit, calculate_deposit, calculate_installment
from doc_report import create_doc_report
from excel_report import create_excel_report

# Разметка интерфейса
layout = [
    [sg.Text("Сумма кредита/вклада/рассрочки:"), sg.InputText(key='-AMOUNT-', size=(20,1))],
    [sg.Text("Процентная ставка (%):"), sg.InputText(key='-RATE-', size=(20,1))],
    [sg.Text("Срок (месяцев):"), sg.InputText(key='-MONTHS-', size=(20,1))],
    
    [sg.Button("Рассчитать"), sg.Button("Сохранить в DOCX"), sg.Button("Сохранить в Excel"), sg.Button("Выход")],
    
    [sg.Text("Результаты расчетов", size=(30, 1), font='Any 12 bold')],
    [sg.Text("Ежемесячный платеж: "), sg.Text("", key='-MONTHLY_PAYMENT-')],
    [sg.Text("Общая сумма выплат/полученная сумма: "), sg.Text("", key='-TOTAL_PAYMENT-')],
    [sg.Text("Начисленные проценты: "), sg.Text("", key='-INTEREST_EARNED-')]
]

window = sg.Window("Банковские услуги", layout)

# Основной цикл программы
while True:
    event, values = window.read()
    
    if event == sg.WINDOW_CLOSED or event == "Выход":
        break
    
    if event == "Рассчитать":
        try:
            amount = float(values['-AMOUNT-'])
            rate = float(values['-RATE-'])
            months = int(values['-MONTHS-'])

            # Вычисление результатов
            credit_result = calculate_credit(amount, rate, months)
            deposit_result = calculate_deposit(amount, rate, months)

            # Обновление GUI с результатами
            window['-MONTHLY_PAYMENT-'].update(f"{credit_result[0]:.2f} руб.")
            window['-TOTAL_PAYMENT-'].update(f"{credit_result[1]:.2f} руб.")
            window['-INTEREST_EARNED-'].update(f"{deposit_result[1]:.2f} руб.")
        
        except ValueError:
            sg.popup_error("Введите корректные данные!")

    if event == "Сохранить в DOCX":
        create_doc_report(credit_result, deposit_result)
        sg.popup("Отчет сохранен в формате DOCX!")

    if event == "Сохранить в Excel":
        create_excel_report(credit_result, deposit_result)
        sg.popup("Отчет сохранен в формате Excel!")

window.close()
~~~
Когда пользователь нажимает на кнопку "Сохранить в DOCX" или "Сохранить в Excel", программа вызывает соответствующую функцию для создания отчетов.
После создания отчетов появляется всплывающее окно (с помощью sg.popup()), которое уведомляет пользователя о том, что отчет был успешно сохранен.


Код по doc report
```python
from docx import Document

def create_doc_report(credit_result, deposit_result, file_name="report.docx"):
    doc = Document()
    doc.add_heading("Отчет по банковским услугам", 0)
    
    doc.add_heading("Кредит", level=1)
    doc.add_paragraph(f"Ежемесячный платеж: {credit_result[0]:.2f} руб.")
    doc.add_paragraph(f"Общая сумма выплат: {credit_result[1]:.2f} руб.")
    
    doc.add_heading("Вклад", level=1)
    doc.add_paragraph(f"Общая сумма на счете: {deposit_result[0]:.2f} руб.")
    doc.add_paragraph(f"Начисленные проценты: {deposit_result[1]:.2f} руб.")
    
    doc.save(file_name)
```
Мы создаем новый объект документа с помощью Document().
Добавляем заголовок с помощью add_heading().
Используем метод add_paragraph() для добавления текста с расчетами для кредита и вклада в отчет.
В конце файл сохраняется с именем bank_report.docx на диск с помощью метода save().

Код по excel report 
```python
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
```
Создаем новый Excel файл с помощью openpyxl.Workbook().
Получаем активный лист с помощью wb.active.
Вставляем заголовки и расчеты для кредита и вклада в ячейки с помощью простого обращения к ячейкам по индексам (например, sheet['A1']).
После того как данные добавлены, файл сохраняется с именем bank_report.xlsx с помощью метода wb.save().

![Alt text](Screenshot_20250403_125715.png)

# Список литературы
[Python модули и пакеты](https://habr.com/ru/articles/718828/)

[PySimpleGUI](https://www.pysimplegui.com/)
