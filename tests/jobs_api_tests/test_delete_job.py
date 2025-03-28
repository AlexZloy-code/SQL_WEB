from requests import delete, get


BASE_URL = "http://127.0.0.1:8000"

API = 'api/v2'

print("Удаление несуществующей работы")
job_id = 0
print(delete(f"{BASE_URL}/{API}/jobs/{job_id}").json())
print('\n\n\n')

print("Удаление работы с неверным типом id")
print(delete(f"{BASE_URL}/{API}/jobs/string").json())
print('\n\n\n')

print("Удаление работы")
job_id = 1
print(delete(f"{BASE_URL}/{API}/jobs/{job_id}").json())
print('\n\n\n')

print("Проверка существования работы")
print(get(f"{BASE_URL}/{API}/jobs/{job_id}").json())