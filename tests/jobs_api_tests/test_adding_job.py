from requests import post, get
from pprint import pprint as p
from datetime import datetime

from werkzeug.security import generate_password_hash


BASE_URL = "http://127.0.0.1:8000/"

API = 'api/v2'

print("Пустой запрос")
data = {}
print(post(f"{BASE_URL}/{API}/jobs", json=data).json())
print('\n\n\n')

print("Поле start_date отсутсвует")
data = {
    "id": 20,
    "team_leader_id": 4,
    "job": "Working hard",
    "work_size": 100,
    "collaborators": "1, 2, 3",
    "send_date": None,
    "is_finished": False
}
print(post(f"{BASE_URL}/{API}/jobs", json=data).json())
print('\n\n\n')

print("Поле id отсутсвует")
data = {
    "id": 20,
    "team_leader_id": 4,
    "job": "Working hard",
    "work_size": 100,
    "collaborators": "1, 2, 3",
    "start_date": datetime.datetime.now().isoformat(),
    "send_date": None,
    "is_finished": False
}
print(post(f"{BASE_URL}/{API}/jobs", json=data).json())
print('\n\n\n')

print("Существующая работа")
data = {
    "id": 1,
    "team_leader_id": 1,
    "job": "Deployment of residential modules 1 and 2",
    "work_size": 15,
    "collaborators": "2, 3",
    "start_date": datetime.now(),
    "send_date": None,
    "is_finished": False,
}
print(post(f"{BASE_URL}/{API}/jobs", json=data).json())
print('\n\n\n')

print("Создание пользователя")
job_id = 999
data = {
    "id": job_id,
    "team_leader_id": 1,
    "job": "Deployment of residential modules 1 and 2",
    "work_size": 15,
    "collaborators": "2, 3",
    "start_date": datetime.now(),
    "send_date": None,
    "is_finished": False,
}
print(post(f"{BASE_URL}/{API}/jobs", json=data).json())
print('\n\n\n')

print("Проверка создания работы")
p(get(f"{BASE_URL}/{API}/jobs/").json())
print('\n\n\n')

print("Одна эта созданая рыбота")
p(get(f"{BASE_URL}/{API}/jobs/{job_id}").json())
