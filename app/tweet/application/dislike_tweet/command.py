from app.common.command import Command
from dataclasses import dataclass
from uuid import UUID


@dataclass
class DislikeTweet(Command):
    tweet_id: UUID
    disliked_user_id: UUID
