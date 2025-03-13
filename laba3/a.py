#без рекурсии
def split_iterative(lst, n):
    result = [[] for _ in range(n)]  # Создаем n пустых списков
    for i, item in enumerate(lst):   # Распределяем элементы по спискам,enumerate это инструмент для итерации по спискам,когда нужно и индекс и значение
        result[i % n].append(item) #вычесляет остаток деления индекса i  на n
    return result
# с рекурсией 
def split_recursive(lst, n, index=0):
    if index >= len(lst):  # Базовый случай: если дошли до конца списка
        return [[] for _ in range(n)]  # Возвращаем n пустых списков
    # Рекурсивно вызываем функцию для оставшейся части списка
    result = split_recursive(lst, n, index + 1)
    # Добавляем текущий элемент в соответствующую часть
    result[index % n].insert(0,lst[index])
    return result
print(split_iterative([1, 2, 3, 4, 5], 3)) 
print(split_recursive([1, 2, 3, 4, 5], 3))   
#без рекурсии
def calculate_v_iterative(n):
    if n == 1 or n == 2:  # Базовые случаи
        return 0
    elif n == 3:
        return 1.5
    
    v = [0] * (n + 1)  # Инициализация списка для хранения значений
    v[1] = 0
    v[2] = 0
    v[3] = 1.5
    
    for i in range(4, n + 1):  # Вычисляем значения по формуле
        v[i] = ((i + 1) / (i**2 + 1)) * v[i-1] - v[i-2] * v[i-3]
    
    return v[n]
#с рекурсией
def calculate_v_recursive(n):
    if n == 1 or n == 2:  # Базовые случаи
        return 0
    elif n == 3:
        return 1.5
    else:  # Рекурсивный случай
        return ((n + 1) / (n**2 + 1)) * calculate_v_recursive(n-1) - calculate_v_recursive(n-2) * calculate_v_recursive(n-3)
print(calculate_v_iterative(5))  
print(calculate_v_recursive(5))  