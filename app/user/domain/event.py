from app.event.event import DomainEvent
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from app.user.domain.model import UserCredential


@dataclass
class UserCreated(DomainEvent):
    screen_id: str
    screen_name: Optional[str]
    bio: Optional[str]


@dataclass
class UserLoggedIn(DomainEvent):
    pass


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


@dataclass
class PasswordChanged(DomainEvent):
    new_credential: "UserCredential"
