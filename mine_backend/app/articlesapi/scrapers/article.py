import abc
import json
from dataclasses import dataclass, asdict
from typing import List, Optional


class Node(abc.ABC):
    pass


@dataclass(frozen=True)
class TextNode(Node):
    text: str


@dataclass(frozen=True)
class ImageNode(Node):
    src: str
    caption: Optional[str] = None


@dataclass(frozen=True)
class VideoNode(Node):
    src: str


@dataclass(frozen=True)
class Article:
    title: str
    description: str
    image_src: Optional[str]

    content_nodes: List[Node]


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
