from app.event.event import IntegrationEvent
from dataclasses import dataclass
from uuid import UUID


@dataclass
class TweetPosted(IntegrationEvent):
    tweet_id: UUID
    tweeted_user_id: UUID
