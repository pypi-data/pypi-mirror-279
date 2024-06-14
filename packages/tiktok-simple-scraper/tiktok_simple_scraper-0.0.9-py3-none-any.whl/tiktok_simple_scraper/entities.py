import abc
import datetime
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Dict

from pydantic import BaseModel


class PostType(Enum):
    VIDEO = 'VIDEO'
    IMAGE = 'IMAGE'
    TEXT = 'TEXT'
    ALBUM = 'ALBUM'


class ReactionType(Enum):
    UNKNOWN = 'UNKNOWN'
    LIKE = 'LIKE'
    CARE = 'CARE'
    DISLIKE = 'DISLIKE'
    WOW = 'WOW'
    ANGRY = 'ANGRY'
    LOVE = 'LOVE'
    HAHA = 'HAHA'
    MAYBE = 'MAYBE'
    PRAISE = 'PRAISE'
    APPRECIATION = 'APPRECIATION'
    SAD = 'SAD'


class SocialMedia(Enum):
    TIKTOK = 'TIKTOK'


@dataclass
class Reaction:
    type: ReactionType
    count: int


class Sentiments(BaseModel):
    positive: float
    negative: float
    neutral: float


class Comment(BaseModel):
    text: str
    user: str
    date: datetime.datetime
    url: str
    reactions: List[Reaction]
    replies: List['Comment']
    sentiments: Optional[Sentiments] = None
    user_name: Optional[str] = None
    user_metadata: Optional[Dict] = None
    score: Optional[float] = None


class Post(BaseModel):
    id: str
    sec_id: Optional[str] = None
    url: str
    hashtags: List[str]
    text: str
    type: PostType
    date: Optional[datetime.datetime]
    reactions: List[Reaction]
    comments: List[Comment]
    reaction_count: int
    share_count: Optional[int] = 0
    view_count: Optional[int] = 0
    total_comments: Optional[int] = 0


class Account(BaseModel):
    name_to_show: str
    id: str
    sec_uid: str
    followers_count: int
    following_count: int
    heart_count: int
    video_count: int
    friend_count: int
    posts: List[Post]
    title: str
    language: str
    region: str = None
    url: Optional[str] = None
    metadata: Optional[Dict] = None
    bio_link: Optional[str] = None
    avatar: Optional[str] = None
    signature: Optional[str] = None




class Company(BaseModel):
    name: str
    accounts: List[Account]


class UserPassCredentials(BaseModel):
    username: str
    password: str


class ScrapeCallbacks(abc.ABC):
    @abc.abstractmethod
    def on_account_scrape_start(self, social_media: SocialMedia, account_id: str) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def on_account_scrape_end(self, social_media: SocialMedia, account: Account) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def on_new_post(self, social_media: SocialMedia, post: Post) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def on_get_comments_start(self, social_media: SocialMedia, post_url: str, page: int = 0) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def on_get_comments_ends(self, social_media: SocialMedia, post_id: str, comments: List[Comment]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def on_success_login(self) -> None:
        raise NotImplementedError()


@dataclass
class ScraperOptions:
    most_old_date: Optional[datetime.datetime]
    check_account_in_storage: bool
    max_comments_per_post: int
    callbacks: Optional[ScrapeCallbacks]
