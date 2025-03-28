from requests import post, get
from pprint import pprint as p
from datetime import datetime

from werkzeug.security import generate_password_hash


BASE_URL = "http://127.0.0.1:8000/"


print("Пустой запрос")
data = {}
print(post(f"{BASE_URL}/api/users", json=data).json())
print('\n\n\n')

print("Поле modified_date отсутсвует")
data = {
    "id": 6,
    "surname": "Sanders",
    "name": "Teddy",
    "age": 27,
    "position": "programmer",
    "speciality": "IT specialist",
    "address": "module_2",
    "email": "sanders@mars.org",
    "hashed_password": generate_password_hash("teddy_bear27"),
}
print(post(f"{BASE_URL}/api/users", json=data).json())
print('\n\n\n')

print("Поле id отсутсвует")
data = {
    "surname": "Sanders",
    "name": "Teddy",
    "age": 27,
    "position": "programmer",
    "speciality": "IT specialist",
    "address": "module_2",
    "email": "sanders@mars.org",
    "hashed_password": generate_password_hash("teddy_bear27"),
    "modified_date": datetime.datetime.now().isoformat(),
}
print(post(f"{BASE_URL}/api/users", json=data).json())
print('\n\n\n')

print("Неверный тип шифровки")
data = {
    "id": 6,
    "surname": "Sanders",
    "name": "Teddy",
    "age": 27,
    "position": "programmer",
    "speciality": "IT specialist",
    "address": "module_2",
    "email": "sanders@mars.org",
    "hashed_password": generate_password_hash("teddy_bear27", method="pbkdf2:sha1"),
    "modified_date": datetime.datetime.now().isoformat(),
}
print(post(f"{BASE_URL}/api/users", json=data).json())
print('\n\n\n')

print("Существующий пользователь")
data = {
    "id": 1,
    "surname": "Sanders",
    "name": "Teddy",
    "age": 27,
    "position": "programmer",
    "speciality": "IT specialist",
    "address": "module_2",
    "email": "sanders@mars.org",
    "hashed_password": generate_password_hash("teddy_bear27"),
    "modified_date": datetime.datetime.now().isoformat(),
}
print(post(f"{BASE_URL}/api/users", json=data).json())
print('\n\n\n')

print("Создание пользователя")
user_id = 999
data = {
    "id": user_id,
    "surname": "Sanders",
    "name": "Teddy",
    "age": 27,
    "position": "programmer",
    "speciality": "IT specialist",
    "address": "module_2",
    "email": "sanders@mars.org",
    "hashed_password": generate_password_hash("teddy_bear27"),
    "modified_date": datetime.datetime.now().isoformat(),
}
print(post(f"{BASE_URL}/api/users", json=data).json())
print('\n\n\n')

print("Проверка создания пользователя")
p(get(f"{BASE_URL}/api/users/").json())
print('\n\n\n')

print("Один этот созданый пользователь")
p(get(f"{BASE_URL}/api/users/{user_id}").json())
