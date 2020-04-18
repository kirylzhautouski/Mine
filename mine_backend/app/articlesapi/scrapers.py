import requests
from bs4 import BeautifulSoup


class TheFlowScraper:

    @staticmethod
    def scrap_article(link):
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')

        title = soup.find('h1', class_='article__title')
        description = soup.find('div', class_='article__descr')
        text = soup.find('div', class_='article__text')

        article = {
            'title': title.text,
            'description': description.text,
            'text': text.text.strip(),
        }

        return article
