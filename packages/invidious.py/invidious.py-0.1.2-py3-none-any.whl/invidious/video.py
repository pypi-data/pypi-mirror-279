from dataclasses import dataclass, field
from typing import List

from .model import Model

@dataclass
class Video(Model):
    """Base Video class. Have maximum options."""

    title: str=""
    videoId: str=""
    author: str=""
    authorId: str=""
    authorUrl: str=""
   
    description: str=""
    descriptionHtml: str=""

    lengthSeconds: int=0

    viewCount: int=0
    likeCount: int=0
    dislikeCount: int=0
    rating: int=0

    published: int=0
    publishedText: str=""

    genre: str=""
    genreUrl: str=""

    paid: bool=False
    premium: bool=False
    liveNow: bool=False
    isListed: bool=False
    isUpcoming: bool=False
    allowRatings: bool=False
    isFamilyFriendly: bool=False

    videoThumbnails: List[dict]=field(
        default_factory=lambda: list()
    )
    storyboards: List[dict]=field(
        default_factory=lambda: list()
    )
    adaptiveFormats: List[dict]=field(
        default_factory=lambda: list()
    )
    formatStreams: List[dict]=field(
        default_factory=lambda: list()
    )

    keywords: List[str]=field(
        default_factory=lambda: list()
    )
    captions: List[dict]=field(
        default_factory=lambda: list()
    )
    allowedRegions: List[str]=field(
        default_factory=lambda: list()
    )
    recommendedVideos: List[dict]=field(
        default_factory=lambda: list()
    )

