from dataclasses import dataclass, field
from typing import List

from .model import Model

@dataclass
class ChannelItem(Model):
    """ChannelItem class. Used in search."""

    author: str=""
    authorId: str=""
    authorUrl: str=""
    authorThumbnails: List[dict]=field(
        default_factory=lambda: list()
    )

    subCount: int=0
    videoCount: int=0

    description: str=""
    descriptionHtml: str=""

