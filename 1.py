"""
1. Ознакомиться с некоторые интересными API. 
https://docs.ozon.ru/api/seller/ https://developers.google.com/youtube/v3/getting-started https://spoonacular.com/food-api

2. Потренируйтесь делать запросы к API. Выберите публичный API, который вас интересует, и 
потренируйтесь делать API-запросы с помощью Postman. Поэкспериментируйте с различными типами запросов и 
попробуйте получить различные типы данных.

3. Сценарий Foursquare
Напишите сценарий на языке Python, который предложит пользователю ввести интересующую его 
категорию (например, кофейни, музеи, парки и т.д.).

5. Используйте API Foursquare для поиска заведений в указанной категории.

6. Получите название заведения, его адрес и рейтинг для каждого из них.
Скрипт должен вывести название и адрес и рейтинг каждого заведения в консоль.
"""

import requests
import json

# Задание  2

# Базовый URL API
base_url = "https://v2.jokeapi.dev/joke"

# Функция для фильтрации нежелательных шуток
def filter_joke(joke):
    flags = joke.get("flags", {})
    if flags.get("nsfw") or flags.get("racist") or flags.get("sexist"):
        return False
    return True

# Получение случайной шутки
def get_random_joke():
    response = requests.get(f"{base_url}/Any")
    if response.status_code == 200:
        joke = response.json()
        if filter_joke(joke):
            print(json.dumps(joke, indent=2))
        else:
            print("Filtered out an inappropriate joke.")
    else:
        print(f"Failed to fetch joke. Status code: {response.status_code}")

# Получение шутки по категории
def get_joke_by_category(category):
    response = requests.get(f"{base_url}/{category}")
    if response.status_code == 200:
        joke = response.json()
        if filter_joke(joke):
            print(json.dumps(joke, indent=2))
        else:
            print("Filtered out an inappropriate joke.")
    else:
        print(f"Failed to fetch joke. Status code: {response.status_code}")

# Основная функция для выполнения запросов
def main():
    print("Получение случайной шутки:")
    get_random_joke()

    print("\nПолучение шутки по категории (Programming):")
    get_joke_by_category("Programming")

    print("\nПолучение шутки по категории (Misc):")
    get_joke_by_category("Misc")

if __name__ == "__main__":
    main()


# Задание 3, 5  и 6

import requests
import json

# Ваши учетные данные API
client_id = "__"
client_secret = "__"

# Конечная точка API
endpoint = "https://api.foursquare.com/v3/places/search"

# Ввод пользователя
city = input("Введите название города: ")
category = input("Введите категорию заведения (например, кофейни, музеи, парки и т.д.): ")

# Параметры запроса
params = {
    'near': city,
    'query': category,
    'limit': 10  # Ограничение на количество результатов, можно изменить при необходимости
}

headers = {
    "Accept": "application/json",
    "Authorization": "fsq3V3AFHzvqod5PVkb9j5ptfec29VfLTGG2XbHrQEGC8bI="
}

# Запрос к API
response = requests.get(endpoint, params=params, headers=headers)

# Проверка успешности запроса API
if response.status_code == 200:
    print("Успешный запрос API!")
    data = response.json()  # Парсим JSON-ответ в словарь Python
    venues = data["results"]  # Получаем список мест из данных ответа
    
    # Проверка, есть ли найденные заведения
    if venues:
        for venue in venues:
            name = venue.get("name", "Не указано")
            location = venue.get("location", {})
            address = location.get("address", "Адрес не указан")
            rating = venue.get("rating", "Рейтинг не указан")  # Обратите внимание на получение рейтинга
            print(f"Название: {name}")
            print(f"Адрес: {address}")
            print(f"Рейтинг: {rating}")
            print("\n")
    else:
        print("Заведения не найдены.")
else:
    print("Запрос API завершился неудачей с кодом состояния:", response.status_code)
    print(response.text)
