from __future__ import annotations

from abc import ABC, abstractmethod
from app.common.aggregate import EventSourcedAggregate
from app.user.domain.event import (
    BioUpdated,
    FollowedUser,
    PasswordChanged,
    UnfollowedUser,
    UserLoggedIn,
    UsernameUpdated,
)
from dataclasses import dataclass
from datetime import datetime
from passlib.hash import argon2
from typing import Optional, Set
from uuid import UUID


class UserAggregate(ABC, EventSourcedAggregate):
    @abstractmethod
    def login(self, password: str) -> None:
        pass

    @abstractmethod
    def update_username(self, new_username: str) -> None:
        pass

    @abstractmethod
    def update_bio(self, new_bio: str) -> None:
        pass

    @abstractmethod
    def change_password(self, old_password: str, new_credential: UserCredential) -> None:
        pass

    @abstractmethod
    def follow_user(self, user_to_follow: UUID) -> None:
        pass

    @abstractmethod
    def unfollow_user(self, user_to_unfollow: UUID) -> None:
        pass


class UserCredential(ABC):
    hash_algorithm: str

    @staticmethod
    @abstractmethod
    def hash(new_password: str) -> UserCredential:
        pass

    @abstractmethod
    def verify(self, password: str) -> bool:
        pass


@dataclass
class Argon2UserCredential(UserCredential):
    hash_algorithm = "argon2"

    hashed_password: str

    @staticmethod
    def hash(new_password: str) -> UserCredential:
        return Argon2UserCredential(argon2.hash(new_password))

    def verify(self, password: str) -> bool:
        return argon2.verify(password, self.hashed_password)


@dataclass
class User(UserAggregate):
    screen_id: str
    username: str
    bio: Optional[str]
    following: Set[UUID]
    credential: UserCredential
    last_login: datetime

    def login(self, password: str) -> None:
        if not self.credential.verify(password):
            raise ValueError("Password does not match")

        self._update(UserLoggedIn())

    def _handle_user_logged_in(self, event: UserLoggedIn) -> None:
        self.last_login = event.occurred_at

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

    def change_password(self, old_password: str, new_credential: UserCredential) -> None:
        if not self.credential.verify(old_password):
            raise ValueError("Password does not match")

        self._update(PasswordChanged(new_credential))

    def _handle_password_changed(self, event: PasswordChanged) -> None:
        self.credential = event.new_credential

    def follow_user(self, user_to_follow: UUID) -> None:
        self._update(FollowedUser(user_to_follow))

    def _handle_followed_user(self, event: FollowedUser) -> None:
        self.following.add(event.followed_user_id)

    def unfollow_user(self, user_to_unfollow: UUID) -> None:
        self._update(UnfollowedUser(user_to_unfollow))

    def _handle_unfollowed_user(self, event: UnfollowedUser) -> None:
        self.following.remove(event.unfollowed_user_id)
