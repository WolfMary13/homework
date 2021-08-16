# Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex-новости. Для парсинга
# использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.


from fake_headers import Headers
from lxml import html
import pandas as pd
import requests
import datetime


class Article:
    def __init__(self):
        self.resources = []
        self.titles = []
        self.links = []
        self.dates = []

    def news_data_frame(self):
        return pd.DataFrame({
            "Resource": self.resources,
            "Title": self.titles,
            "Link": self.links,
            "Date or Time": self.dates
        })


def news_parser_yandex(root: html.etree.Element):
    article = Article()
    article.resources = root.xpath(f'//article/div[3]/div[1]/div/span[1]/a/text()')
    title_elements = root.xpath(f'//article/div[1]/div/a')
    article.titles = [title_element.text_content() for title_element in title_elements]
    article.links = [title_element.get('href') for title_element in title_elements]
    article.dates = root.xpath(f'//article/div[3]/div[1]/div/span[2]/text()')
    return article


def news_parser_lenta(root: html.etree.Element):
    article = Article()
    article_xpath = '//*[@id="root"]/section[2]/div/div/*/*/*/section/*'
    article.titles = [title.replace('\xa0', ' ') for title in
                      root.xpath(f'{article_xpath}/a/h3/text()')]
    article.dates = root.xpath(f'{article_xpath}/div/span/text()')
    for j in article.dates:
        if j == 'Сегодня':
            article.dates = datetime.datetime.today().strftime("%d-%m-%Y")

    article.links = ['https://lenta.ru/' + link.get('href') for link in
                     root.xpath(f'{article_xpath}/a[@class="titles"]')]
    article.resources = ['lenta.ru' for title in article.titles]
    return article


def news_parser_mailru(root: html.etree.Element):
    article = Article()
    article_xpath = '//div[contains(@class, "newsitem")]'
    article.resources = root.xpath(f'{article_xpath}/div/span[2]/text()')
    article.titles = root.xpath(f'{article_xpath}/span[2]/a/span/text()')
    article.links = [title.get('href') for title in root.xpath(f'{article_xpath}/span[2]/a')]
    article.dates = root.xpath(f'{article_xpath}/div/span[1]/text()')
    return article


headers = Headers(headers=True).generate()


news_yandex = news_parser_yandex(html.fromstring(requests.get('https://yandex.ru/news', headers=headers).text))
news_lenta = news_parser_lenta(html.fromstring(requests.get('https://lenta.ru', headers=headers).text))
news_mailru = news_parser_mailru(html.fromstring(requests.get('https://news.mail.ru', headers=headers).text))

df = pd.concat([
    news_yandex.news_data_frame(),
    news_lenta.news_data_frame(),
    news_mailru.news_data_frame(),
], axis=0, ignore_index=True)

df.to_csv('All_news.csv')
