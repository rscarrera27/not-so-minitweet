from app.common.command_handler import CommandHandler
from app.event.publisher import IntegrationEventPublisher
from app.tweet.application.like_tweet.command import LikeTweet
from app.tweet.domain.repository import TweetAggregateRepository
from app.tweet.event import TweetLiked


class LikeTweetCommandHandler(CommandHandler[LikeTweet]):
    def __init__(self, tweet_aggregate_repo: TweetAggregateRepository, event_publisher: IntegrationEventPublisher):
        self.tweet_aggregate_repo = tweet_aggregate_repo
        self.event_publisher = event_publisher

    async def handle(self, command: LikeTweet) -> None:
        tweet = await self.tweet_aggregate_repo.find_by_id(command.tweet_id)
        tweet.like(command.liked_user_id)
        await self.tweet_aggregate_repo.save(tweet)
        await self.event_publisher.publish(TweetLiked(command.tweet_id, command.liked_user_id))
