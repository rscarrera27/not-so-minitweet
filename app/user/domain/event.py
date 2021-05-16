from app.event.event import DomainEvent
from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class UserCreated(DomainEvent):
    screen_id: str
    screen_name: Optional[str]
    bio: Optional[str]


@dataclass
class FollowedUser(DomainEvent):
    followed_user_id: UUID


@dataclass
class UnfollowedUser(DomainEvent):
    unfollowed_user_id: UUID


@dataclass
class UsernameUpdated(DomainEvent):
    username: str


@dataclass
class BioUpdated(DomainEvent):
    bio: str
