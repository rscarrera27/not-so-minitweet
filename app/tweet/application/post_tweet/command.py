from dataclasses import dataclass
from uuid import UUID


@dataclass
class PostTweet:
    text: str
    tweeted_user_id: UUID
