from dataclasses import dataclass, field
from typing import List

from .model import Model

@dataclass
class RecommendedVideo(Model):
    """RecommendedVideo class. Used in recommendedVideos option of Video class."""

    title: str=""
    videoId: str=""
    author: str=""
    authorId: str=""
    authorUrl: str=""
    
    lengthSeconds: int=0
    viewCount: int=0
    viewCountText: str=""

    videoThumbnails: List[dict]=field(
        default_factory=lambda: list()
    )

