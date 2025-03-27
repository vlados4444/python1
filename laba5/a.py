import requests
import json

# Генератор для получения данных с API
def fetch_data_from_api(api_url, page_limit=3):
    for page in range(1, page_limit + 1):  # Получаем данные с нескольких страниц
        url = f"{api_url}?_page={page}"
        response = requests.get(url)  # Делаем запрос к API
        if response.status_code == 200:  # Если запрос успешен
            yield response.json()  # Возвращаем данные
        else:
            print(f"Ошибка при запросе: {response.status_code}")
            break

# Функция для обработки данных
def process_data(data):
    # Фильтруем пользователей, чьи имена начинаются с 'C'
    filtered_data = filter(lambda x: x['name'].startswith('C'), data)
    
    # Извлекаем имена и email этих пользователей
    mapped_data = map(lambda x: {'name': x['name'], 'email': x['email']}, filtered_data)
    
    # Возвращаем обработанные данные как список
    return list(mapped_data)

# Сохраняем данные в файл
def save_to_file(data, filename="output.json"):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Основная функция
def main():
    api_url = "https://jsonplaceholder.typicode.com/users"
    
    # Собираем данные с нескольких страниц API
    collected_data = []
    for data in fetch_data_from_api(api_url):
        collected_data.extend(data)  # Добавляем данные с каждой страницы
    
    # Обрабатываем собранные данные
    processed_data = process_data(collected_data)
    
    # Сохраняем обработанные данные в файл
    save_to_file(processed_data)
    print(f"Обработанные данные сохранены в файл 'output.json'.")

if __name__ == "__main__":
    main()
    x=fetch_data_from_api("https://jsonplaceholder.typicode.com/users")
    print (next(x))
    print(type(x))