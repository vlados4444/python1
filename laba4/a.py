# Замыкание для проверки диапазона
def range_closure(min_val, max_val):
    # Замыкание возвращает функцию, которая проверяет диапазон
    def inner(x):
        if x < min_val or x > max_val:
            raise ValueError(f"Аргумент {x} вне допустимого диапазона [{min_val}, {max_val}]")
        elif x > min_val or x < max_val:    
            print(f"Аргумент {x} в допустимом диапазоне [{min_val}, {max_val}]")
        return x  # Возвращаем аргумент, если он в диапазоне
    return inner

def error_handler_decorator(func):#Оборачивает функцию в try,перехватывает любые исключения и выводит сообщение об ошибке,Возвращает None в случае ошибки. 
    # Декоратор возвращает функцию-обертку
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None  # Возвращаем None в случае ошибки
    return wrapper
# Функция, которую мы будем использовать
def my_function(x):
    return x * 2

# Создаем замыкание с диапазоном [0, 100]
check_range = range_closure(6, 10)
# Применяем декоратор к замыканию
safe_check_range = error_handler_decorator(check_range)

# Тестируем 
print(safe_check_range(5))