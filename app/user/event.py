from app.event.event import IntegrationEvent
from dataclasses import dataclass
from uuid import UUID


@dataclass
class FollowedUser(IntegrationEvent):
    user_id: UUID
    followed_user_id: UUID


@dataclass
class UnfollowedUser(IntegrationEvent):
    user_id: UUID
    unfollowed_user_id: UUID
