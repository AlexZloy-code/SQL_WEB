from werkzeug.security import generate_password_hash

from requests import put, get
from pprint import pprint as p
from datetime import datetime


BASE_URL = "http://127.0.0.1:8000/"


print("Редактирование несуществующей работы")
user_id = 0
print(put(f"{BASE_URL}/api/users/{user_id}").json())
print('\n\n\n')

print("Редактирование работы с неверным типом id")
print(put(f"{BASE_URL}/api/users/string").json())
print('\n\n\n')

print('Редактирование без поля modified_date')
user_id = 1
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
print(put(f"{BASE_URL}/api/users/{user_id}", json=data).json())
print('\n\n\n')

print("Редактирование пользователя с неправильным типом шифровки пароля")
user_id = 1
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
    "modified_date": datetime.now().isoformat(),
}
print(put(f"{BASE_URL}/api/users/{user_id}", json=data).json())
print('\n\n\n')

print("Редактирование работы")
user_id = 2
data = {
    "id": 2,
    "surname": "Sanders",
    "name": "Teddy",
    "age": 27,
    "position": "programmer",
    "speciality": "IT specialist",
    "address": "module_2",
    "email": "sanders_manders@mars.org",  # уникальная почта из-за предыдущих тестов
    "hashed_password": generate_password_hash("teddy_bear27"),
    "modified_date": datetime.now().isoformat(),
}
print(put(f"{BASE_URL}/api/users/{user_id}", json=data).json())
print('\n')

print("Показ изменённой работы")
print(get(f"{BASE_URL}/api/users/{user_id}").json())