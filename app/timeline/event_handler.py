from app.event.handler import IntegrationEventHandler
from app.tweet.event import (
    Retweeted,
    TweetDisliked,
    TweetLiked,
    TweetPosted,
    Unretweeted,
)
from app.user.event import FollowedUser, UnfollowedUser


class TweetPostedEventHandler(IntegrationEventHandler[TweetPosted]):
    async def handle(self, event: TweetPosted) -> None:
        pass


class TweetLikedEventHandler(IntegrationEventHandler[TweetLiked]):
    async def handle(self, event: TweetLiked) -> None:
        pass


class RetweetedEventHandler(IntegrationEventHandler[Retweeted]):
    async def handle(self, event: Retweeted) -> None:
        pass


class TweetDislikedEventHandler(IntegrationEventHandler[TweetDisliked]):
    async def handle(self, event: TweetDisliked) -> None:
        pass


class UnretweetedEventHandler(IntegrationEventHandler[Unretweeted]):
    async def handle(self, event: Unretweeted) -> None:
        pass


class FollowedUserEventHandler(IntegrationEventHandler[FollowedUser]):
    async def handle(self, event: FollowedUser) -> None:
        pass


class UnfollowedUserEventHandler(IntegrationEventHandler[UnfollowedUser]):
    async def handle(self, event: UnfollowedUser) -> None:
        pass
