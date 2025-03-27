from requests import post, get
from pprint import pprint as p
from datetime import datetime


BASE_URL = "http://127.0.0.1:8000/"


print("Пустой запрос")
data = {}
print(post(f"{BASE_URL}/api/jobs", json=data).json())
print('\n\n\n')

print("Поле is_finished отсутсвует")
data = {
    "id": 1,
    "team_leader_id": 4,
    "job": "Working hard",
    "work_size": 100,
    "collaborators": "1, 2, 3",
    "start_date": datetime.now().isoformat(),
}
print(post(f"{BASE_URL}/api/jobs", json=data).json())
print('\n\n\n')

print("Поле id отсутсвует")
data = {
    "is_finish": True,
    "team_leader_id": 4,
    "job": "Working hard",
    "work_size": 100,
    "collaborators": "1, 2, 3",
    "start_date": datetime.now().isoformat(),
}
print(post(f"{BASE_URL}/api/jobs", json=data).json())
print('\n\n\n')

print("Существующая работа")
data = {
    "id": 1,
    "team_leader_id": 4,
    "job": "Working hard",
    "work_size": 100,
    "collaborators": "1, 2, 3",
    "start_date": datetime.now().isoformat(),
    "end_date": None,
    "is_finished": False
}
print(post(f"{BASE_URL}/api/jobs", json=data).json())
print('\n\n\n')

print("создание работы")
job_id = 999
data = {
    "id": job_id,
    "team_leader_id": 4,
    "job": "Working hard",
    "work_size": 100,
    "collaborators": "1, 2, 3",
    "start_date": datetime.now().isoformat(),
    "end_date": None,
    "is_finished": False
}
print(post(f"{BASE_URL}/api/jobs", json=data).json())
print('\n\n\n')

print("проверка создания работы")
p(get(f"{BASE_URL}/api/jobs/").json())
print('\n\n\n')

print("одна эта созданая работа")
p(get(f"{BASE_URL}/api/jobs/{job_id}").json())