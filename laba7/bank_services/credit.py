from .base import FinancialService

class Credit(FinancialService):
    def calculate(self):
        monthly_rate = self._rate / 12 / 100
        payment = self._amount * monthly_rate / (1 - (1 + monthly_rate) ** -self._term)
        return [round(payment, 2)] * self._term

    @property
    def total_payment(self):
        return round(sum(self.calculate()), 2)

    def __len__(self):
        return self._term

    def __eq__(self, other):
        return self.total_payment == other.total_payment
