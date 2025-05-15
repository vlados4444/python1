from .base import FinancialService

class Installment(FinancialService):
    def calculate(self):
        return [round(self._amount / self._term, 2)] * self._term

    @property
    def total_payment(self):
        return round(sum(self.calculate()), 2)

    def __len__(self):
        return self._term

    def __eq__(self, other):
        return self.total_payment == other.total_payment
