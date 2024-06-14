from dataclasses import dataclass, field
from typing import List

from .playlist_item import PlaylistItem
from .model import Model

@dataclass
class ChannelPlaylists(Model):
    channel_id: str=""
    continuation: str=""
    playlists: List[PlaylistItem]=field(
        default_factory=lambda: list()
    )

    current: int=-1

    def __iter__(self) -> "ChannelPlaylists":
        return self

    def __next__(self) -> PlaylistItem:
        self.current += 1
        if self.current < len(self.playlists):
            return self.playlists[self.current]
        raise StopIteration

    def __len__(self) -> int:
        return len(self.playlists)

