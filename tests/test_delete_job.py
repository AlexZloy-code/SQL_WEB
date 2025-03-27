from requests import delete, get
from pprint import pprint as p


BASE_URL = "http://127.0.0.1:8000/"


print("Удаление несуществующей работы")
job_id = 0
print(delete(f"{BASE_URL}api/jobs/{job_id}").json())
print('\n\n\n')

print("Удаление работы с неверным типом id")
print(delete(f"{BASE_URL}api/jobs/string").json())
print('\n\n\n')

print("Удаление работы")
job_id = 1
print(delete(f"{BASE_URL}api/jobs/{job_id}").json())
print('\n\n\n')

print("Проверка существования работы")
print(get(f"{BASE_URL}api/jobs/{job_id}").json())