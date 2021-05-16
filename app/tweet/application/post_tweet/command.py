from app.common.command import Command
from dataclasses import dataclass
from uuid import UUID


@dataclass
class PostTweet(Command):
    text: str
    tweeted_user_id: UUID
