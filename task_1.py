# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую
# собранные вакансии в созданную БД.
# 3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта


import search_vacancy as searcher
from pymongo.database import Database
from pymongo import MongoClient
from fake_headers import Headers
from bs4 import BeautifulSoup
import requests
import lxml


# Добавить данные или обновить данные

def add_or_update_vacancy(db: Database, vacancy: searcher.Vacancy):
    db.vacancies.update_one(
        {'link': vacancy.link},
        {'$set': {
            'link': vacancy.link,
            'company': vacancy.company,
            'salary': {
                'from': vacancy.salary.price_from,
                'to': vacancy.salary.price_to,
                'currency': vacancy.salary.currency
            },
            'name': vacancy.name,
            'source': vacancy.source
        }},
        upsert=True
    )


headers = Headers(headers=True).generate()
search_query = input("Интересующая вакансия: ")

hh_url = f'https://novosibirsk.hh.ru/vacancies/{search_query}'
hh_soup = BeautifulSoup(requests.get(hh_url, headers=headers).text, 'lxml')

sj_url = f'https://nsk.superjob.ru/vakansii/{search_query}.html'
sj_soup = BeautifulSoup(requests.get(sj_url, headers=headers).text, 'lxml')

all_vacancies = searcher.scrap_hh(hh_soup) + searcher.scrap_sj(sj_soup)

client = MongoClient('localhost', 27017)
db_ = client['lesson3']

for j in all_vacancies:
    add_or_update_vacancy(db_, j)
    print(j)