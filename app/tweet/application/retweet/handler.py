from app.common.command_handler import CommandHandler
from app.event.publisher import IntegrationEventPublisher
from app.tweet.application.retweet.command import Retweet
from app.tweet.domain.repository import TweetAggregateRepository
from app.tweet.event import Retweeted


class RetweetCommandHandler(CommandHandler[Retweet]):
    def __init__(self, tweet_aggregate_repo: TweetAggregateRepository, event_publisher: IntegrationEventPublisher):
        self.tweet_aggregate_repo = tweet_aggregate_repo
        self.event_publisher = event_publisher

    async def handle(self, command: Retweet) -> None:
        tweet = await self.tweet_aggregate_repo.find_by_id(command.tweet_id)
        tweet.retweet(command.retweeted_user_id)
        await self.tweet_aggregate_repo.save(tweet)
        await self.event_publisher.publish(Retweeted(tweet.id, command.retweeted_user_id))
