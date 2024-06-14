from dataclasses import dataclass, field
from typing import List

from .comment import Comment
from .model import Model

@dataclass
class CommentsList(Model):
    """Comments list class."""

    videoId: str=""
    commentCount: int=0
    continuation: str=""

    comments: List[Comment]=field(
        default_factory=lambda: list()
    )

