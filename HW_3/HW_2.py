"""
1. Установите MongoDB на локальной машине, а также зарегистрируйтесь в онлайн-сервисе.
2. Загрузите данные который вы получили на предыдущем уроке путем скрейпинга сайта с 
помощью Buautiful Soup в MongoDB и создайте базу данных и коллекции для их хранения.
3. Поэкспериментируйте с различными методами запросов.
"""

import json
from pymongo import MongoClient

# Подключение к серверу MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Выбор базы данных и коллекции
db = client['library']
collection = db['books']

# Чтение файла JSON с указанием кодировки
with open('books_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Проверка типа данных
if isinstance(data, list):
    # Если data - это список, оставляем его как есть
    pass
elif isinstance(data, dict) and 'features' in data:
    # Если data - это словарь и содержит ключ 'features', то используем data['features']
    data = data['features']
else:
    raise ValueError("Unexpected data format")

# Проверка наличия данных в коллекции и добавление данных, если коллекция пустая
if collection.count_documents({}) == 0:
    collection.insert_many(data)

# Вывод первой записи в коллекции
first_doc = collection.find_one()

# Вывод объекта JSON
pretty_json = json.dumps(first_doc, indent=4, default=str)
print(pretty_json)

# Получение количества документов в коллекции с помощью функции count_documents()
count = collection.count_documents({})
print(f'Число записей в базе данных: {count}')

# Найти количество книг с ценой выше 50
count_expensive_books = collection.count_documents({"price": {"$gt": 50}})
print(f'Число книг с ценой выше 50: {count_expensive_books}')

# Найти количество книг с определённым количеством в наличии
count_in_stock_books = collection.count_documents({"quantity": {"$gt": 0}})
print(f'Число книг в наличии: {count_in_stock_books}')

# Найти количество книг, содержащих слово "history" в описании
count_history_books = collection.count_documents({"description": {"$regex": "history", "$options": "i"}})
print(f'Число книг с "history" в описании: {count_history_books}')

"""# Обновить цену всех книг, которые стоят меньше 20, на 10%
collection.update_many(
    {"price": {"$lt": 20}},
    {"$mul": {"price": 1.10}}
)

# Найти количество книг, цена которых была обновлена
count_updated_books = collection.count_documents({"price": {"$lt": 22}})
print(f'Число книг с ценой менее 22 (после обновления цен): {count_updated_books}')

# Удалить все книги, у которых количество равно нулю
collection.delete_many({"quantity": 0})

# Найти количество книг, у которых количество равно нулю
count_deleted_books = collection.count_documents({"quantity": 0})
print(f'Число книг с количеством 0 (после удаления): {count_deleted_books}')

# Получить количество всех книг
count_all_books = collection.count_documents({})
print(f'Число всех книг в коллекции: {count_all_books}')"""