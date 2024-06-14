from dataclasses import dataclass, field
from typing import List

from .model import Model

@dataclass
class PlaylistItem(Model):
    """PlaylistItem class. Used in search."""

    title: str=""
    playlistId: str=""
    playlistThumbnail: str=""
    author: str=""
    authorId: str=""
    authorUrl: str=""
    authorVerified: bool=False
    videoCount: int=0

    videos: List[dict]=field(
        default_factory=lambda: list()
    )

