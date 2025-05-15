from abc import ABC, abstractmethod

class FinancialService(ABC):
    def __init__(self, amount: float, term: int, rate: float):
        self._amount = amount
        self._term = term
        self._rate = rate

    @abstractmethod
    def calculate(self):
        pass

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value

    def __str__(self):
        return f"{self.__class__.__name__} на сумму {self.amount} сроком {self._term} мес."

    def __repr__(self):
        return self.__str__()
