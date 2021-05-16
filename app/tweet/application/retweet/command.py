from app.common.command import Command
from dataclasses import dataclass
from uuid import UUID


@dataclass
class Retweet(Command):
    tweet_id: UUID
    retweeted_user_id: UUID
