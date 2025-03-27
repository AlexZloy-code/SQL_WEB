from requests import put, get
from pprint import pprint as p
from datetime import datetime


BASE_URL = "http://127.0.0.1:8000/"


print("Редактирование несуществующей работы")
job_id = 0
print(put(f"{BASE_URL}/api/jobs/{job_id}").json())
print('\n\n\n')

print("Редактирование работы с неверным типом id")
print(put(f"{BASE_URL}/api/jobs/string").json())
print('\n\n\n')

print("Редактирование работы")
job_id = 2
data = {
    "id": 2,
    "team_leader_id": 4,
    "job": "Working hard",
    "work_size": 100,
    "collaborators": "1, 2, 3",
    "start_date": datetime.now().isoformat(),
    "end_date": None,
    "is_finished": False
}
print(put(f"{BASE_URL}/api/jobs/{job_id}", json=data).json())
print('\n')

print("Показ изменённой работы")
print(get(f"{BASE_URL}/api/jobs/{job_id}").json())