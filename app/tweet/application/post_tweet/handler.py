from app.event.publisher import IntegrationEventPublisher
from app.tweet.application.post_tweet.command import PostTweet
from app.tweet.domain.model import Tweet
from app.tweet.domain.repository import TweetAggregateRepository
from app.tweet.event import TweetPosted


class PostTweetCommandHandler:
    def __init__(self, tweet_aggregate_repo: TweetAggregateRepository, event_publisher: IntegrationEventPublisher):
        self.tweet_aggregate_repo = tweet_aggregate_repo
        self.event_publisher = event_publisher

    async def handle(self, command: PostTweet):
        new_tweet = Tweet.new(command.text, command.tweeted_user_id)
        await self.tweet_aggregate_repo.save(new_tweet)
        await self.event_publisher.publish(TweetPosted(new_tweet.id, command.tweeted_user_id))
