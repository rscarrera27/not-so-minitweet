from abc import ABC, abstractmethod
from app.tweet.domain.model import TweetAggregate
from typing import Optional
from uuid import UUID


class TweetAggregateRepository(ABC):
    @abstractmethod
    async def save(self, tweet: TweetAggregate) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, tweet_id: UUID) -> Optional[TweetAggregate]:
        pass
