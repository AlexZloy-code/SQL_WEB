from requests import delete, get
from pprint import pprint as p


BASE_URL = "http://127.0.0.1:8000/"


print("удаление несуществующей работы")
job_id = 0
print(delete(f"{BASE_URL}api/jobs/{job_id}").json())
print('\n\n\n')

print("удаление работы с неверным типом id")
print(delete(f"{BASE_URL}api/jobs/string").json())
print('\n\n\n')

print("удаление работы")
job_id = 1
print(delete(f"{BASE_URL}api/jobs/{job_id}").json())
print('\n\n\n')

print("проверка существования работы")
print(get(f"{BASE_URL}api/jobs/{job_id}").json())