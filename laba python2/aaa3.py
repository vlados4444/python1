num = 452022  # Начинаем с первого числа больше 452021
count = 0  # Счетчик найденных чисел
while count < 5:  # Ищем 5 чисел
    divisors = [d for d in range(2, num) if num % d == 0]
    # divisors_ = []
    # for d in range(2, num):
    #     if num % d == 0:
    #         divisors_.append(d) # Находим делители
    if divisors:  # Если есть делители
        M = min(divisors) + max(divisors)  # Считаем M
        if M % 7 == 3:  # Проверяем условие
            print(num, M)  # Выводим число и M
            count += 1  # Увеличиваем счетчик

    num += 1  # Берем следующее число