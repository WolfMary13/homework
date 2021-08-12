# Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.

# Зачем писать функцию, если можно сделать однострочным запросом?

from pymongo.database import Database
from pymongo import MongoClient

user_salary = input('Зарплата от: ')
client = MongoClient('localhost', 27017)
db = client['lesson3']


def salary_search(needed_salary):
    result = db.vacancies.find({"salary.from": {'$gt': needed_salary}})
    for j in result:
        print(j)


print(salary_search(user_salary))
