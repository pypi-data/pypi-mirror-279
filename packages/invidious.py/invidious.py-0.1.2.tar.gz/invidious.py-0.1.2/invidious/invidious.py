from enum import Enum

from .types import (RecommendedVideo, CommentsList,
                    PlaylistItem, ChannelItem,
                    ShortVideo, VideoItem,
                    Comment, Channel, Video, ChannelPlaylists)
from .enums.sortby import SortBy, SortByTime
from .enums.content_type import ContentType
from .enums.trending import Trending
from .enums.duration import Duration
from .enums.feauter import Feauter
from .enums.iv_date import Date
from .config import *

from typing import Optional
import multiprocessing
import requests
import logging

class Invidious:
    """
    Base Invidious class.
    """

    def __init__(self, timeout: int=5,
        mirrors: list=list(), check_best_mirror: bool=True) -> None:
        """
        :enable_logger - Enable or disable logs.
        :timeout - request wait timeout.
        :mirrors - list of mirrors you want to use.
        :check_best_mirror - use multiprocessing library for check fast responsible mirror
        """
        self.logger = self._init_logger()
        self.timeout = timeout
        self.check_best_mirror = check_best_mirror

        if len(mirrors) == 0: self.mirrors = MIRRORS
        else: self.mirrors = mirrors

        self.manager = multiprocessing.Manager()
        self.wmirrors = self.manager.list()
        self.mprocs = list()

    def _init_logger(self) -> logging.Logger:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            '%Y-%m-%d %H:%M:%S'
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def _mirror_request(self, mirror: str) -> None:
        api_url = mirror+"/api/v1/trending"
        try: 
            response = requests.get(
                api_url, headers=HEADERS,
                timeout=self.timeout
            )
        except:
            self.logger.warning(f"{mirror} doesn't response.")
            return

        if response.status_code == 200:
            self.logger.info(f"Mirror {mirror} is work.")
            self.wmirrors.append(mirror)
        else:
            self.logger.warning(f"{mirror} status code - {response.status_code}.")

    def _update_mirrors(self) -> None:
        self.wmirrors[:] = []
        for mirror in self.mirrors:
            self._mirror_request(mirror)
            if len(self.wmirrors) > 0:
                return

    def _update_mirrors_mp(self) -> None:
        self.wmirrors[:] = []
        for mirror in self.mirrors:
            process = multiprocessing.Process(target=self._mirror_request, args=(mirror,))
            self.mprocs.append(process)
            process.start()
        
        while len(self.wmirrors)==0 and len(multiprocessing.active_children())>0: pass
        
        for proc in self.mprocs:
            proc.kill()

    def _get_working_mirror(self) -> str:
        if len(self.wmirrors) == 0: 
            if self.check_best_mirror:
                self._update_mirrors_mp()
            else:
                self._update_mirrors()
        return self.wmirrors[0]

    def _request(self, url: str) -> Optional[dict | list]:
        mirror = self._get_working_mirror()
        try: 
            response = requests.get(
                mirror+url, headers=HEADERS,
                timeout=self.timeout
            )
        except Exception as e:
            self.logger.error(f"{e}")
            return 
        if response.status_code == 200: return response.json()
        elif response.status_code == 429:
            self.logger.error(f"Too many requests - {url}.")
        elif response.status_code == 404:
            self.logger.error(f"Page not found - {url}.")

    def _make_args(self, args: dict=dict()) -> str:
        argstr = ""; index = 0
        for key, value in args.items():
            if not value or value == "": continue
            subchar = "?" if index == 0 else "&"
            if isinstance(value, Enum):
                value = value.value
            if isinstance(value, list):
                value = ",".join(value)
            argstr += f"{subchar}{key}={value}"
            index += 1

        return argstr

    def search(self, query: str, page: int=0,
               sort_by: SortBy=SortBy.RELEVANCE,
               duration: Optional[Duration]=None,
               date: Optional[Date]=None, 
               ctype: ContentType=ContentType.ALL,
               feauters: list[Feauter]=list(),
               region: str="") -> list[ChannelItem | VideoItem | PlaylistItem]:
        """
        Invidious search method. Return list with VideoItem, ChannelItem, PlaylistItem.

        query: your search query
        page: number of page (default: 0)
        sort_by: enums.SortBy - Sort items by any parameter (default: SortBy.RELEVANCE)
        date: Optional[enums.Date] (default: None) 
        duration: Optional[enums.Duration] - Video duration (default: None)
        ctype: enums.ContentType (default: ContentType.ALL)
        feauters: list[enums.Feauter] (default: list())
        region: ISO 3166 country code (default: US)
        """
        args = {
            'q'         : query, 
            'page'      : page,
            'sort_by'   : sort_by,
            'duration'  : duration,
            'date'      : date,
            'type'      : ctype,
            'feauters'  : feauters,
            'region'    : region
        }
        req = f"/api/v1/search" + self._make_args(args)

        response = self._request(req)
        if not response: return list()

        items = list()
        types = {
            'channel' : ChannelItem,
            'video' : VideoItem,
            'playlist' : PlaylistItem
        }
        for item in response:
            class_obj = None
            if item['type'] in types.keys():
                class_obj = types[item['type']]
                items.append(
                    class_obj.from_json(item)
                )
        
        return items

    def get_all_channel_playlists(self, channel_id: str) -> Optional[ChannelPlaylists]:
        """
        Return types.ChannelPlaylists with types.PlaylistItem list.

        channel_id: str - Channel ID
        """
        playlists = list()
        
        channel_playlists = self.get_channel_playlists(channel_id)
        if not channel_playlists: return 

        def include_playlists(playlists: list, items: ChannelPlaylists) -> None:
            for item in items:
                playlists.append(item)
        
        include_playlists(playlists, channel_playlists)
        continuation = channel_playlists.continuation

        while continuation != "":
            channel_playlists= self.get_channel_playlists(
                channel_id,
                continuation=continuation
            )
            if not channel_playlists: break
            continuation = channel_playlists.continuation

            include_playlists(playlists, channel_playlists)
        return ChannelPlaylists(channel_id, playlists=playlists)

    def get_channel_playlists(
            self, channel_id: str,
            continuation: Optional[str]=None,
            sort_by: SortByTime=SortByTime.LAST) -> Optional[ChannelPlaylists]:
        """
        Return types.ChannelPlaylists with types.PlaylistItem list.

        channel_id: str - Channel ID
        continuation: Optional[str] - A continuation token to get the next chunk of items (default: None)
        sort_by: enums.SortByTime - Sort order filter (default: enums.SortByTime.LAST)
        """
        args = {
            'continuation' : continuation,
            'sort_by' : sort_by
        }
        req = f"/api/v1/channels/{channel_id}/playlists" + self._make_args(args)
        response = self._request(req)
        if not response or isinstance(response, list): return
        
        playlists = list()
        for item in response['playlists']:
            playlists.append(
                PlaylistItem.from_json(item)
            )
        response['playlists'] = playlists
        response['channel_id'] = channel_id
        
        return ChannelPlaylists.from_json(response)
 
    def get_comments(self, videoId: str, sort_by: str="", 
                     source: str="", continuation: str="") -> Optional[CommentsList]:
        """
        Invidious get_comments method. Return CommentsList by videoId

        sort_by: "top", "new" (default: top)
        source: "youtube", "reddit" (default: youtube)
        continuation: like next page of comments
        """
        args = {
            'sorty_by' : sort_by,
            'source' : source,
            'continuation' : continuation
        }
        req = f"/api/v1/comments/{videoId}" + self._make_args(args)

        response = self._request(req)
        if not response or isinstance(response, list): return
        
        clist = CommentsList.from_json(response)
        cmts = clist.comments

        comments = list()
        for item in cmts:
            if not isinstance(item, dict): continue
            comments.append(Comment.from_json(item))
        clist.comments = comments

        return clist

    def get_video(self, video_id: str, region: str="US") -> Optional[Video]:
        """
        Return Video object by id.
        
        video_id: str - Video ID
        region: str - ISO 3166 country code (default: US).
        """
        args = {
            'region' : region
        }
        req = f"/api/v1/videos/{video_id}" + self._make_args(args)

        response = self._request(req)
        if not response or isinstance(response, list): return
            
        raw_rec_videos = response['recommendedVideos']
        recommended_videos = list()
        for item in raw_rec_videos:
            recommended_videos.append(
                RecommendedVideo.from_json(item)
            )
        response['recommendedVideos'] = recommended_videos

        return Video.from_json(response)

    def get_channel(self, authorId: str, sort_by: str="") -> Optional[Channel]:
        """
        Invidious get_channel method. Return Channel by id.
        
        authorId: str - Channel ID.
        sort_by: sorting channel videos. [newest, oldest, popular] (default: newest).
        """
        args = {
            'sort_by' : sort_by
        }
        req = f"/api/v1/channels/{authorId}" + self._make_args(args)

        response = self._request(req)
        if not response or isinstance(response, list): return

        raw_latest_videos = response['latestVideos']
        latest_videos = list()
        for item in raw_latest_videos:
            latest_videos.append(VideoItem.from_json(item))
        response['latestVideos'] = latest_videos 

        return Channel.from_json(response)

    def get_popular(self) -> list:
        """
        Invidious get_popular method. Return list with ShortVideo.
        """
        req = f"/api/v1/popular"

        response = self._request(req)
        if not response: return list()
            
        videos = list()
        for item in response:
            videos.append(ShortVideo.from_json(item))

        return videos

    def get_trending(self,
                     trending_type: Optional[Trending]=None,
                     region: str="") -> list:
        """
        Invidious get_trending method. Return list with VideoItem.

        trending_type: enums.Trending - Trending category
        region: str - ISO 3166 country code (default: US).
        """
        args = {
            'type' : trending_type,
            'region' : region
        }
        req = f"/api/v1/trending" + self._make_args(args)
        
        response = self._request(req)
        if not response: return list() 
            
        videos = list()
        for item in response:
            videos.append(VideoItem.from_json(item))

        return videos 

if __name__ == "__main__":
    iv = Invidious()
    print(iv.wmirrors)



