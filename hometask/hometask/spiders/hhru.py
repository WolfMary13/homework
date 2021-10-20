import scrapy
from scrapy.http import HtmlResponse
from hometask.items import HometaskItem
from hometask.salary import Salary


def vacancy_parse(response: HtmlResponse):
    name = response.css('h1[data-qa="vacancy-title"]::text').extract_first()
    salary_raw = response.css('span[data-qa="bloko-header-2"]::text').extract_first()
    salary = Salary(salary_raw, is_superjob=False)
    yield HometaskItem(name=name,
                       salary_from=salary.price_from,
                       salary_to=salary.price_to,
                       salary_currency=salary.currency,
                       source='hh.ru',
                       link=response.url)


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['https://hh.ru/']
    start_urls = ['https://izhevsk.hh.ru/search/vacancy?area=&st=searchVacancy&text=python']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.bloko-button[data-qa="pager-next"]::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy = response.css(
            'a.bloko-link[data-qa="vacancy-serp__vacancy-title"]::attr(href)'
        ).extract()

        for link in vacancy:
            yield response.follow(link, callback=vacancy_parse)
