from requests import get
from pprint import pprint as p


BASE_URL = "http://127.0.0.1:8000/"

print('Все пользователи')
p(get(BASE_URL + 'api/users').json())
print('\n\n\n')

print('Корректный запрос пользователи')
print(get(BASE_URL + 'api/users/1').json())
print('\n\n\n')

print('Запрос несуществующей пользователи')
print(get(BASE_URL + 'api/users/1000').json())
print('\n\n\n')

print('Строка вместо индекса в запросе без преобразования в json')
print(get(BASE_URL + 'api/users/t'))
print('\n\n\n')

print('Строка вместо индекса в запросе с преобразованием в json')
print(get(BASE_URL + 'api/users/t').json())
