import requests
from itertools import dropwhile
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

from app.articlesapi.scrapers.exceptions import UnknownChildType, UnknownTagName
from app.articlesapi.scrapers.nodes import create_image_node, create_text_node, create_video_node


class TheFlowScraper:

    @staticmethod
    def _scrap_image_div(tag):
        image = tag.find('img')
        if image:
            try:
                possible_caption = next(dropwhile(lambda x: x.name == 'br' or x.name == 'img', tag.children))

                if isinstance(possible_caption, NavigableString):
                    caption = str(possible_caption).strip()
                else:
                    caption = None
            except StopIteration:
                caption = None

            return create_image_node('https://the-flow.ru' + image['src'], caption)
        else:
            return None

    @staticmethod
    def _scrap_em(tag):
        return create_text_node(tag.text.strip())

    @staticmethod
    def _scrap_br(tag):
        return None

    @staticmethod
    def _scrap_video_iframe(tag):
        embed_video_src = tag['src']
        video_id = embed_video_src.replace('//www.youtube.com/embed/', '')
        return create_video_node(f'https://youtube.com/watch?v={video_id}')

    _TAG_SCRAPPERS = {
        'em': _scrap_image_div.__func__,
        'br': _scrap_br.__func__,
        'div': _scrap_image_div.__func__,
        'iframe': _scrap_video_iframe.__func__,
    }

    @staticmethod
    def _scrap_tag(tag):
        scrap_function = TheFlowScraper._TAG_SCRAPPERS.get(tag.name)
        if scrap_function:
            return scrap_function(tag)

        raise UnknownTagName(f'Unknown tag: {tag.name}')

    @staticmethod
    def _scrap_content(content_soup):
        nodes = []

        for child in content_soup.children:
            node = None

            if isinstance(child, Tag):
                node = TheFlowScraper._scrap_tag(child)
            elif isinstance(child, NavigableString):
                node = create_text_node(str(child).strip())
            else:
                raise UnknownChildType(f'Unknown child: {child}')

            if node:
                nodes.append(node)

        return nodes

    @staticmethod
    def _scrap_summary(article_soup):
        title = article_soup.find('h1', class_='article__title')
        description = article_soup.find('div', class_='article__descr')
        image = article_soup.find('img', itemprop='contentUrl')

        summary = {
            'title': title.text,
            'description': description.text,
        }

        if image:
            summary['imageSrc'] = 'https://the-flow.ru' + image.get('src')

        return summary

    @staticmethod
    def _build_soup(link):
        page = requests.get(link)
        return BeautifulSoup(page.content, 'html.parser')

    @staticmethod
    def scrap_article(link):
        soup = TheFlowScraper._build_soup(link)

        article = {}
        article.update(TheFlowScraper._scrap_summary(soup))

        content = soup.find('div', class_='article__text').find('p')
        article['contentNodes'] = TheFlowScraper._scrap_content(content)

        return article

    @staticmethod
    def get_article_summary(link):
        soup = TheFlowScraper._build_soup(link)
        return TheFlowScraper._scrap_summary(soup)
