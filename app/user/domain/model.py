from __future__ import annotations

from abc import ABC, abstractmethod
from app.common.aggregate import EventSourcedAggregate
from app.user.domain.event import (
    BioUpdated,
    FollowedUser,
    UnfollowedUser,
    UserCreated,
    UsernameUpdated,
)
from dataclasses import dataclass
from typing import Optional, Set
from uuid import UUID, uuid4


class UserAggregate(ABC, EventSourcedAggregate):
    @staticmethod
    @abstractmethod
    def new(screen_id: str, username: str, bio: Optional[str]) -> UserAggregate:
        pass

    @abstractmethod
    def update_username(self, new_username: str) -> None:
        pass

    @abstractmethod
    def update_bio(self, new_bio: str) -> None:
        pass

    @abstractmethod
    def follow_user(self, user_to_follow: UUID) -> None:
        pass

    @abstractmethod
    def unfollow_user(self, user_to_unfollow: UUID) -> None:
        pass


@dataclass
class User(UserAggregate):
    screen_id: str
    username: str
    bio: Optional[str]
    following: Set[UUID]

    @staticmethod
    def new(screen_id: str, username: str, bio: Optional[str]) -> UserAggregate:
        new_user = User(uuid4(), -1, screen_id, username, bio, set())
        new_user._update(UserCreated(screen_id, username, bio))

        return new_user

    def _handle_user_created(self, event: UserCreated) -> None:
        return

    def update_username(self, new_username: str) -> None:
        if len(new_username) >= 10:
            raise ValueError("Too Long")

        self._update(UsernameUpdated(new_username))

    def _handle_username_updated(self, event: UsernameUpdated) -> None:
        self.username = event.username

    def update_bio(self, new_bio: str) -> None:
        if len(new_bio) >= 200:
            raise ValueError("Too long")

        self._update(BioUpdated(new_bio))

    def _handle_bio_updated(self, event: BioUpdated) -> None:
        self.bio = event.bio

    def follow_user(self, user_to_follow: UUID) -> None:
        self._update(FollowedUser(user_to_follow))

    def _handle_followed_user(self, event: FollowedUser) -> None:
        self.following.add(event.followed_user_id)

    def unfollow_user(self, user_to_unfollow: UUID) -> None:
        self._update(UnfollowedUser(user_to_unfollow))

    def _handle_unfollowed_user(self, event: UnfollowedUser) -> None:
        self.following.remove(event.unfollowed_user_id)
