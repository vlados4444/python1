import PySimpleGUI as sg
import json
import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict


# ===== Исключения =====
class FinancialTrackerError(Exception):
    pass

class InvalidAmountError(FinancialTrackerError):
    pass

class InvalidCategoryError(FinancialTrackerError):
    pass

class InvalidDateError(FinancialTrackerError):
    pass


# ===== Абстрактный класс (ПОЛИМОРФИЗМ) =====
class Record(ABC):
    """Абстрактный класс для записи расхода/дохода"""
    
    @abstractmethod
    def to_dict(self) -> Dict:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict) -> 'Record':
        pass


# ===== Расход =====
class Expense(Record):
    """Класс расхода с ИНКАПСУЛЯЦИЕЙ"""

    def __init__(self, amount: float, category: str, description: str, date: str):
        self.__amount = amount
        self.__category = category
        self.__description = description
        self.__date = date

    @property
    def amount(self) -> float:
        return self.__amount

    @property
    def category(self) -> str:
        return self.__category

    @property
    def description(self) -> str:
        return self.__description

    @property
    def date(self) -> str:
        return self.__date

    def to_dict(self) -> Dict:
        return {
            'amount': self.__amount,
            'category': self.__category,
            'description': self.__description,
            'date': self.__date
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Expense':
        return cls(
            amount=data['amount'],
            category=data['category'],
            description=data['description'],
            date=data['date']
        )


# ===== Доход =====
class Income(Record):
    """Класс дохода с ИНКАПСУЛЯЦИЕЙ"""

    def __init__(self, income: float, source: str, description: str, date: str):
        self.__income = income
        self.__source = source
        self.__description = description
        self.__date = date

    @property
    def income(self) -> float:
        return self.__income

    @property
    def source(self) -> str:
        return self.__source

    @property
    def description(self) -> str:
        return self.__description

    @property
    def date(self) -> str:
        return self.__date

    def to_dict(self) -> Dict:
        return {
            'income': self.__income,
            'source': self.__source,
            'description': self.__description,
            'date': self.__date
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Income':
        return cls(
            income=data['income'],
            source=data['source'],
            description=data['description'],
            date=data['date']
        )


# ===== Финансовый трекер =====
class FinancialTracker:
    """Менеджер расходов и доходов с ИНКАПСУЛЯЦИЕЙ"""

    def __init__(self, data_file: str = 'expenses.json'):
        self.__data_file = data_file
        self.__records: List[Record] = []  # Записи о расходах и доходах
        self.__categories = [
            'Еда', 'Транспорт', 'Жилье', 'Развлечения',
            'Здоровье', 'Образование', 'Одежда', 'Другое'
        ]
        self.load_data()

    @property
    def categories(self) -> List[str]:
        return self.__categories.copy()

    def add_expense(self, amount: float, category: str, description: str, date: str) -> None:
        try:
            amount = float(amount)
            #if amount <= 0:
             #   raise InvalidAmountError("Сумма должна быть положительной")

            if category not in self.__categories:
                raise InvalidCategoryError("Неверная категория")

            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                raise InvalidDateError("Неверный формат даты. Используйте YYYY-MM-DD")

            expense = Expense(amount, category, description, date)
            self.__records.append(expense)
            self.save_data()

        except ValueError:
            raise InvalidAmountError("Сумма должна быть числом")

    def add_income(self, income: float, source: str, description: str, date: str) -> None:
        try:
            income = float(income)
            #if income <= 0:
             #   raise FinancialTrackerError("Доход должен быть положительным")

            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                raise InvalidDateError("Неверный формат даты. Используйте YYYY-MM-DD")

            income_record = Income(income, source, description, date)
            self.__records.append(income_record)
            self.save_data()

        except ValueError:
            raise FinancialTrackerError("Доход должен быть числом")

    def get_records(self) -> List[Record]:
        return self.__records.copy()

    def get_total_spending(self) -> float:
        return sum(record.income if isinstance(record, Income) else record.amount for record in self.__records)

    def get_spending_by_category(self) -> Dict[str, float]:
        result = {}
        for record in self.__records:
            if isinstance(record, Expense):
                result[record.category] = result.get(record.category, 0) + record.amount
        return result

    def save_data(self) -> None:
        data = [record.to_dict() for record in self.__records]
        with open(self.__data_file, 'w') as f:
            json.dump(data, f, indent=2)

    def load_data(self):
        """Загружает данные из файла, проверяет, какой тип данных в нем (расходы или доходы)."""
        if not os.path.exists(self.__data_file):
            return  # Если файла нет, ничего не загружаем

        try:
            with open(self.__data_file, 'r') as f:
                data = json.load(f)  # Загружаем данные из файла
                for item in data:
                    if 'amount' in item:  # Проверяем, есть ли ключ 'amount', чтобы понять, это расход или доход
                        self.__records.append(Expense.from_dict(item))  # Это расход
                    elif 'income' in item:  # Или это доход
                        self.__records.append(Income.from_dict(item))  # Это доход
        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка при загрузке данных: {e}")
            raise FinancialTrackerError("Ошибка загрузки данных")


# ===== GUI =====
class FinancialTrackerGUI:
    def __init__(self):
        self.tracker = FinancialTracker()
        self.setup_theme()
        self.setup_layout()
        self.window = sg.Window('Финансовый трекер', self.layout, finalize=True)

    def setup_theme(self):
        sg.theme('LightGreen')
        sg.set_options(font=('Arial', 12))

    def setup_layout(self):
        input_frame = [
            [sg.Text('Сумма:'), sg.InputText(key='-AMOUNT-', size=(15, 1))],
            [sg.Text('Категория:'), sg.Combo(self.tracker.categories, key='-CATEGORY-', size=(15, 1), readonly=True)],
            [sg.Text('Описание:'), sg.InputText(key='-DESCRIPTION-', size=(30, 1))],
            [sg.Text('Дата:'), sg.InputText(key='-DATE-', size=(15, 1), default_text=datetime.now().strftime('%Y-%m-%d')),
             sg.CalendarButton('Выбрать', target='-DATE-', format='%Y-%m-%d')],
            [sg.Button('Добавить', key='-ADD-'), sg.Button('Очистить', key='-CLEAR-')]
        ]

        expenses_table = sg.Table(
            values=self.get_table_data(),
            headings=['Дата', 'Категория', 'Сумма', 'Описание'],
            key='-TABLE-',
            auto_size_columns=False,
            col_widths=[10, 15, 10, 20],
            justification='left',
            expand_x=True,
            expand_y=True,
            enable_click_events=True
        )

        stats_frame = [
            [sg.Text('Общие расходы:'), sg.Text('0', key='-TOTAL-')],
            [sg.Text('По категориям:'), sg.Multiline(key='-BY_CATEGORY-', size=(25, 5), disabled=True)]
        ]

        self.layout = [
            [sg.Column(input_frame), sg.VSeparator(), sg.Column(stats_frame)],
            [sg.HSeparator()],
            [expenses_table],
            [sg.Button('Обновить', key='-REFRESH-'), sg.Button('Удалить', key='-DELETE-'), sg.Button('Выход', key='-EXIT-')]
        ]

    def get_table_data(self) -> List[List[str]]:
        return [[record.date, record.source if isinstance(record, Income) else record.category,
                 f"{record.income if isinstance(record, Income) else record.amount:.2f}",
                 record.description] for record in self.tracker.get_records()]

    def update_stats(self):
        total = self.tracker.get_total_spending()
        by_category = self.tracker.get_spending_by_category()
        self.window['-TOTAL-'].update(f"{total:.2f}")
        self.window['-BY_CATEGORY-'].update("\n".join(f"{k}: {v:.2f}" for k, v in by_category.items()))

    def clear_inputs(self):
        self.window['-AMOUNT-'].update('')
        self.window['-CATEGORY-'].update('')
        self.window['-DESCRIPTION-'].update('')
        self.window['-DATE-'].update(datetime.now().strftime('%Y-%m-%d'))

    def run(self):
        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, '-EXIT-'):
                break
            elif event == '-ADD-':
                try:
                    if int(values['-AMOUNT-'])>0:  
                        self.tracker.add_income(
                        values['-AMOUNT-'],
                        values['-CATEGORY-'],
                        values['-DESCRIPTION-'],
                        values['-DATE-']
                    )
                    else:
                        self.tracker.add_expense(
                        values['-AMOUNT-'],
                        values['-CATEGORY-'],
                        values['-DESCRIPTION-'],
                        values['-DATE-']
                    )
                    self.window['-TABLE-'].update(values=self.get_table_data())
                    self.update_stats()
                    self.clear_inputs()
                    sg.popup(f"{self.tracker.get_records()[-1].__class__.__name__} добавлен!", title='Успех')
                except FinancialTrackerError as e:
                    sg.popup_error(str(e), title='Ошибка')
            elif event == '-CLEAR-':
                self.clear_inputs()
            elif event == '-REFRESH-':
                self.window['-TABLE-'].update(values=self.get_table_data())
                self.update_stats()
            elif event == '-DELETE-':
                if values['-TABLE-']:
                    index = values['-TABLE-'][0]
                    records = self.tracker.get_records()
                    del records[index]
                    self.tracker.save_data()
                    self.window['-TABLE-'].update(values=self.get_table_data())
                    self.update_stats()
                    sg.popup('Удалено', title='Успех')

# Запуск GUI
if __name__ == '__main__':
    app = FinancialTrackerGUI()
    app.run()

