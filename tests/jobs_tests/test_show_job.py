from requests import get
from pprint import pprint as p


BASE_URL = "http://127.0.0.1:8000/"

print('Все работы')
p(get(BASE_URL + 'api/jobs').json())
print('\n\n\n')

print('Корректный запрос работы')
print(get(BASE_URL + 'api/jobs/1').json())
print('\n\n\n')

print('Запрос несуществующей работы')
print(get(BASE_URL + 'api/jobs/1000').json())
print('\n\n\n')

print('Строка вместо индекса в запросе без преобразования в json')
print(get(BASE_URL + 'api/jobs/t'))
print('\n\n\n')

print('Строка вместо индекса в запросе с преобразованием в json')
print(get(BASE_URL + 'api/jobs/t').json())

