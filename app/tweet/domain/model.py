from __future__ import annotations

from abc import ABC, abstractmethod
from app.common.aggregate import DirtyCheckedAggregate
from dataclasses import dataclass
from typing import Set
from uuid import UUID, uuid4


class TweetAggregate(ABC, DirtyCheckedAggregate):
    @staticmethod
    @abstractmethod
    def new(text: str, tweeted_user_id: UUID) -> TweetAggregate:
        pass

    @abstractmethod
    def like(self, liked_user_id: UUID) -> None:
        pass

    @abstractmethod
    def retweet(self, retweeted_user_id: UUID) -> None:
        pass

    @abstractmethod
    def dislike(self, disliked_user_id: UUID) -> None:
        pass

    @abstractmethod
    def unretweet(self, unretweeted_user_id: UUID) -> None:
        pass


@dataclass
class Tweet(TweetAggregate):
    text: str
    tweeted_user_id: UUID
    liked_user_ids: Set[UUID]
    retweeted_user_ids: Set[UUID]

    @staticmethod
    def new(text: str, tweeted_user_id: UUID) -> TweetAggregate:
        return Tweet(uuid4(), text, tweeted_user_id, set(), set())

    def like(self, liked_user_id: UUID) -> None:
        if liked_user_id in self.liked_user_ids:
            raise ValueError("Already liked.")

        self.liked_user_ids.add(liked_user_id)

    def retweet(self, retweeted_user_id: UUID) -> None:
        if retweeted_user_id in self.retweeted_user_ids:
            raise ValueError("Already retweeted")

        self.retweeted_user_ids.add(retweeted_user_id)

    def dislike(self, disliked_user_id: UUID) -> None:
        if disliked_user_id in self.liked_user_ids:
            self.liked_user_ids.remove(disliked_user_id)

    def unretweet(self, unretweeted_user_id: UUID) -> None:
        if unretweeted_user_id in self.retweeted_user_ids:
            self.retweeted_user_ids.remove(unretweeted_user_id)
