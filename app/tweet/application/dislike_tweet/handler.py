from app.common.command_handler import CommandHandler
from app.event.publisher import IntegrationEventPublisher
from app.tweet.application.dislike_tweet.command import DislikeTweet
from app.tweet.domain.repository import TweetAggregateRepository
from app.tweet.event import TweetDisliked


class DislikeTweetCommandHandler(CommandHandler[DislikeTweet]):
    def __init__(self, tweet_aggregate_repo: TweetAggregateRepository, event_publisher: IntegrationEventPublisher):
        self.tweet_aggregate_repo = tweet_aggregate_repo
        self.event_publisher = event_publisher

    async def handle(self, command: DislikeTweet) -> None:
        tweet = await self.tweet_aggregate_repo.find_by_id(command.tweet_id)
        tweet.dislike(command.disliked_user_id)
        await self.tweet_aggregate_repo.save(tweet)
        await self.event_publisher.publish(TweetDisliked(command.tweet_id, command.disliked_user_id))
