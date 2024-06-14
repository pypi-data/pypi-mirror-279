from dataclasses import dataclass, field
from typing import List

from .model import Model

@dataclass
class ShortVideo(Model):
    """ShortVideo class. Used in popular videos."""

    title: str=""
    videoId: str=""
    author: str=""
    authorId: str=""
    authorUrl: str=""
    
    lengthSeconds: int=0

    viewCount: int=0
    viewCountText: str=""

    published: int=0
    publishedText: str=""

    videoThumbnails: List[dict]=field(
        default_factory=lambda: list()
    )

