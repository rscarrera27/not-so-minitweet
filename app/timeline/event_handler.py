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
        # TODO: Update timeline read model
        # TODO: Update profile read model
        pass


class TweetLikedEventHandler(IntegrationEventHandler[TweetLiked]):
    async def handle(self, event: TweetLiked) -> None:
        # TODO: Update liked read model
        pass


class RetweetedEventHandler(IntegrationEventHandler[Retweeted]):
    async def handle(self, event: Retweeted) -> None:
        # TODO: Update timeline read model
        # TODO: Update profile read model
        pass


class TweetDislikedEventHandler(IntegrationEventHandler[TweetDisliked]):
    async def handle(self, event: TweetDisliked) -> None:
        # TODO: Update liked read model
        pass


class UnretweetedEventHandler(IntegrationEventHandler[Unretweeted]):
    async def handle(self, event: Unretweeted) -> None:
        # TODO: Update timeline read model
        # TODO: Update profile read model
        pass


class FollowedUserEventHandler(IntegrationEventHandler[FollowedUser]):
    async def handle(self, event: FollowedUser) -> None:
        # TODO: Update timeline read model
        pass


class UnfollowedUserEventHandler(IntegrationEventHandler[UnfollowedUser]):
    async def handle(self, event: UnfollowedUser) -> None:
        # TODO: Update timeline read model
        pass
