from .base import FinancialService

class Deposit(FinancialService):
    def calculate(self):
        return round(self._amount * (1 + self._rate / 100) ** (self._term / 12), 2)

    def __len__(self):
        return self._term

    def __eq__(self, other):
        return self.calculate() == other.calculate()
