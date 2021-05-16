from app.common.command import Command
from dataclasses import dataclass
from uuid import UUID


@dataclass
class Unretweet(Command):
    tweet_id: UUID
    unretweeted_user_id: UUID
