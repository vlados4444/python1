# bank_services.py расчет процентов по кредиту, рассрочке и вкладу
def calculate_credit(principal, rate, months):
    monthly_rate = rate / 100 / 12#преобразует процентную ставку из процента в десятичную дробь
    monthly_payment = principal * monthly_rate / (1 - (1 + monthly_rate) ** -months)
    total_payment = monthly_payment * months
    return monthly_payment, total_payment

def calculate_installment(principal, rate, months):
    # Аналогично кредиту, но без учета начального платежа
    return calculate_credit(principal, rate, months)

def calculate_deposit(principal, rate, months):
    final_amount = principal * (1 + rate / 100) ** months
    interest_earned = final_amount - principal
    return final_amount, interest_earned