from enum import Enum

class SortBy(Enum):
    RELEVANCE: str="relevance"
    RATING: str="rating"
    UPLOAD_DATE: str="upload_date"
    VIEW_COUNT: str="view_count"

class SortByTime(Enum):
    OLDEST: str="oldest"
    NEWEST: str="newest"
    LAST: str="last"


