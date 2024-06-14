from dataclasses import dataclass, field
from typing import List

from .model import Model

@dataclass
class Comment(Model):
    """Comment class."""

    author: str=""
    authorId: str=""
    authorUrl: str=""
    authorThumbnails: List[dict]=field(
        default_factory=lambda: list()
    )
    
    commentId: str=""

    content: str=""
    contentHtml: str=""

    published: int=0
    publishedText: str=""

    likeCount: int=0
    isEdited: bool=False
    authorIsChannelOwner: bool=False
    verified: bool=False


