from requests import delete, get


BASE_URL = "http://127.0.0.1:8000/"


print("Удаление несуществующего полльзователя")
user_id = 0
print(delete(f"{BASE_URL}api/users/{user_id}").json())
print('\n\n\n')

print("Удаление полльзователя с неверным типом id")
print(delete(f"{BASE_URL}api/users/string").json())
print('\n\n\n')

print("Удаление полльзователя")
user_id = 1
print(delete(f"{BASE_URL}api/users/{user_id}").json())
print('\n\n\n')

print("Проверка существования полльзователя")
print(get(f"{BASE_URL}api/users/{user_id}").json())