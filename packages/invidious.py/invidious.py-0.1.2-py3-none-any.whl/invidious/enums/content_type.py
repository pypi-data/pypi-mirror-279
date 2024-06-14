from enum import Enum

class ContentType(Enum):
    VIDEO: str="video"
    PLAYLIST: str="playlist"
    CHANNEL: str="channel"
    ALL: str="all"
