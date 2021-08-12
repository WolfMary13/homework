from bs4 import BeautifulSoup


class Salary:
    def __init__(self, text: str, is_superjob: bool):
        no_price = False
        if len(text) == 0 or is_superjob and text == 'По договорённости':
            no_price = True
            self.price_from = 'Нет данных'
            self.price_to = 'Нет данных'
            self.currency = 'руб.'
        elif text.startswith('от'):
            self.price_from = ''.join(filter(str.isdigit, text))
            self.price_to = '-'
        elif text.startswith('до'):
            self.price_from = 'Нет данных'
            self.price_to = ''.join(filter(str.isdigit, text))
        elif '–' in text:
            from_to = text.split('–')
            self.price_from = ''.join(filter(str.isdigit, from_to[0]))
            self.price_to = ''.join(filter(str.isdigit, from_to[1]))
        else:
            price = ''.join(filter(str.isdigit, text))
            self.price_from = price
            self.price_to = price
        if not no_price:
            chunks = text.split(' ')
            self.currency = chunks[-1]
            if is_superjob:
                self.currency = self.currency.replace('руб./месяц', 'руб.')

    def __str__(self):
        return f"от {self.price_from} до {self.price_to} {self.currency}"


class Vacancy:
    def __init__(self, name, link, salary, company, source):
        self.name = name
        self.link = link
        self.salary = Salary(salary, source == 'superjob.ru')
        self.company = company
        self.source = source

    def __str__(self):
        return f"{self.name}\n{self.company}\n{self.salary.__str__()}\n{self.source}\n{self.link}\n"


def scrap_hh(soup: BeautifulSoup):
    about_vacancy = soup.find_all(class_='vacancy-serp-item')
    vacancies = []
    for i in about_vacancy:
        name = i.find(attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
        link = i.find(attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
        salary_list = [tag.text.replace('\u202f', ' ') for tag in
                       i.find_all(attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})]
        company = i.find(attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text.replace('\xa0', ' ')
        salary = ''
        if len(salary_list) > 0:
            salary = salary_list[0]
        vacancy = Vacancy(name=name, link=link, salary=salary, company=company, source='Head Hunter')
        vacancies.append(vacancy)
    return vacancies


def scrap_sj(soup: BeautifulSoup):
    about_vacancy = soup.find_all(class_='Fo44F QiY08 LvoDO')
    vacancies = []
    for j in about_vacancy:
        name = j.find(class_='_6AfZ9').text
        link = 'https://www.superjob.ru' + j.find(class_='_6AfZ9')['href']
        salary = j.find(class_='_1h3Zg _2Wp8I _2rfUm _2hCDz _2ZsgW').text.replace('\xa0', ' ')
        company = j.find(class_='_205Zx').text
        vacancy = Vacancy(name=name, link=link, salary=salary, company=company, source='Super Job')
        vacancies.append(vacancy)
    return vacancies


