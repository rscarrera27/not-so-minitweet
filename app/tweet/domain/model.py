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


@dataclass
class Tweet(TweetAggregate):
    text: str
    tweeted_user_id: UUID
    liked_user_ids: Set[UUID]

    @staticmethod
    def new(text: str, tweeted_user_id: UUID) -> TweetAggregate:
        return Tweet(uuid4(), text, tweeted_user_id, set())

    def like(self, liked_user_id: UUID) -> None:
        if liked_user_id in self.liked_user_ids:
            raise ValueError("Already liked.")

        self.liked_user_ids.add(liked_user_id)
