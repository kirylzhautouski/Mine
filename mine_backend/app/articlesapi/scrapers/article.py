import abc
import json
from dataclasses import dataclass, asdict
from typing import List, Optional


class Node(abc.ABC):

    def to_dict(self):
        return {
            '@type': self.__class__.__name__,
        }


@dataclass(frozen=True)
class TextNode(Node):
    text: str

    def to_dict(self):
        result = super().to_dict()
        result['text'] = self.text
        return result


@dataclass(frozen=True)
class ImageNode(Node):
    src: str
    caption: Optional[str] = None

    def to_dict(self):
        result = super().to_dict()
        result.update({
            'src': self.src,
            'caption': self.caption,
        })
        return result


@dataclass(frozen=True)
class VideoNode(Node):
    src: str

    def to_dict(self):
        result = super().to_dict()
        result['src'] = self.src
        return result


@dataclass(frozen=True)
class Article:
    title: str
    description: str
    image_src: Optional[str]

    content_nodes: List[Node]

    def to_dict(self):
        result = {
                'title': self.title,
                'description': self.description,
                'imageSrc': self.image_src,
        }
        result['contentNodes'] = list(map(lambda x: x.to_dict(), self.content_nodes))
        return result


class ArticleJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Node):
            result = {
                '@type': o.__class__.__name__,
            }
            result.update(asdict(o))
            return result
        elif isinstance(o, Article):
            return {
                'title': o.title,
                'description': o.description,
                'imageSrc': o.image_src,
                'contentNodes': o.content_nodes
            }
        else:
            return super().default(o)
