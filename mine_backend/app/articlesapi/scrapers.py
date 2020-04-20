import requests
from itertools import dropwhile
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

from app import app


class UnknownChildType(Exception):
    pass


class UnknownTagName(Exception):
    pass


class InvalidTagStructure(Exception):
    pass


class Nodes:

    @staticmethod
    def create_image_node(image_src, caption):
        return {
            '@type': 'ImageNode',
            'src': image_src,
            'caption': caption,
        }

    @staticmethod
    def create_video_node(video_src):
        return {
            '@type': 'VideoNode',
            'src': video_src,
        }

    @staticmethod
    def create_text_node(text):
        if not text:
            return None

        return {
            '@type': 'TextNode',
            'text': text,
        }


class TheFlowScraper:

    @staticmethod
    def __scrap_tag(tag):
        if tag.name == 'em':
            return Nodes.create_text_node(tag.text.strip())
        elif tag.name == 'br':
            return None
        elif tag.name == 'div':
            image = tag.find('img')
            if image:
                try:
                    possible_caption = next(dropwhile(lambda x: x.name == 'br' or x.name == 'img', tag.children))

                    app.logger.info(possible_caption)

                    if isinstance(possible_caption, NavigableString):
                        caption = str(possible_caption).strip()
                    else:
                        caption = None
                except StopIteration:
                    caption = None

                return Nodes.create_image_node('https://the-flow.ru' + image['src'], caption)
            else:
                return None
        elif tag.name == 'iframe':
            return Nodes.create_video_node(tag['src'])
        else:
            raise UnknownTagName(f'Unknown tag: {tag.name}')

    @staticmethod
    def __scrap_content(content):
        nodes = []

        for child in content.children:
            node = None

            if isinstance(child, Tag):
                node = TheFlowScraper.__scrap_tag(child)
            elif isinstance(child, NavigableString):
                node = Nodes.create_text_node(str(child).strip())
            else:
                raise UnknownChildType(f'Unknown child: {child}')

            if node:
                nodes.append(node)

        return nodes

    @staticmethod
    def scrap_article(link):
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')

        title = soup.find('h1', class_='article__title')
        description = soup.find('div', class_='article__descr')
        image = soup.find('img', itemprop='contentUrl')

        content = soup.find('div', class_='article__text').find('p')
        content_nodes = TheFlowScraper.__scrap_content(content)

        article = {
            'title': title.text,
            'description': description.text,
            'imageSrc': 'https://the-flow.ru' + image.get('src'),
            'contentNodes': content_nodes,
        }

        return article
