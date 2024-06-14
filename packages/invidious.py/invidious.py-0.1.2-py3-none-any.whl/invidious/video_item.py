from dataclasses import dataclass, field
from typing import List

from .model import Model

@dataclass
class VideoItem(Model):
    """VideoItem class. Used in search."""

    title: str=""
    videoId: str=""
    author: str=""
    authorId: str=""
    authorUrl: str=""
   
    description: str=""
    descriptionHtml: str=""

    lengthSeconds: int=0
    viewCount: int=0
    published: int=0
    publishedText: str=""

    genre: str=""
    genreUrl: str=""

    premium: bool=False
    liveNow: bool=False
    isUpcoming: bool=False

    videoThumbnails: List[dict]=field(
        default_factory=lambda: list()
    )

