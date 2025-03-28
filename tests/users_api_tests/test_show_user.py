from requests import get
from pprint import pprint as p


BASE_URL = "http://127.0.0.1:8000/"
API = 'api/v2'

print('Все пользователи')
p(get(BASE_URL + API + '/users').json())
print('\n\n\n')

print('Корректный запрос пользователи')
print(get(BASE_URL + API + '/users/1').json())
print('\n\n\n')

print('Запрос несуществующей пользователи')
print(get(BASE_URL + API + '/users/1000').json())
print('\n\n\n')

print('Строка вместо индекса в запросе без преобразования в json')
print(get(BASE_URL + API + '/users/t'))
print('\n\n\n')

print('Строка вместо индекса в запросе с преобразованием в json')
print(get(BASE_URL + API + '/users/t').json())
