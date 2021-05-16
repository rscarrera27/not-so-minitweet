from app.event.event import IntegrationEvent
from dataclasses import dataclass
from uuid import UUID


@dataclass
class TweetPosted(IntegrationEvent):
    tweet_id: UUID
    tweeted_user_id: UUID


@dataclass
class TweetLiked(IntegrationEvent):
    tweet_id: UUID
    liked_user_id: UUID


@dataclass
class Retweeted(IntegrationEvent):
    tweet_id: UUID
    retweeted_user_id: UUID


@dataclass
class TweetDisliked(IntegrationEvent):
    tweet_id: UUID
    disliked_user_id: UUID


@dataclass
class Unretweeted(IntegrationEvent):
    tweet_id: UUID
    unretweeted_user_id: UUID
