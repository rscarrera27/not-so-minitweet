from app.tweet.domain.model import Tweet
from typing import cast
from uuid import uuid4

import pytest


class TestTweetAggregate:
    @pytest.fixture
    def tweet(self):
        return Tweet(uuid4(), "hello", uuid4(), set(), set())

    def test_new(self):
        fake_user_id = uuid4()
        new_tweet = Tweet.new("hello world", fake_user_id)

        new_tweet = cast(Tweet, new_tweet)

        assert new_tweet.text == "hello world"
        assert new_tweet.tweeted_user_id == fake_user_id

    class TestLike:
        def test_with_already_liked_user(self, tweet):
            fake_user_id = uuid4()

            tweet.liked_user_ids.add(fake_user_id)

            with pytest.raises(ValueError):
                tweet.like(fake_user_id)

        def test_with_never_liked_user(self, tweet):
            fake_user_id = uuid4()

            tweet.like(fake_user_id)

            assert fake_user_id in tweet.liked_user_ids
            assert "liked_user_ids" in tweet.pending_changes

    class TestRetweet:
        def test_with_already_retweeted_user(self, tweet):
            fake_user_id = uuid4()

            tweet.retweeted_user_ids.add(fake_user_id)

            with pytest.raises(ValueError):
                tweet.retweet(fake_user_id)

        def test_with_never_retweeted_user(self, tweet):
            fake_user_id = uuid4()

            tweet.retweet(fake_user_id)

            assert fake_user_id in tweet.retweeted_user_ids
            assert "retweeted_user_ids" in tweet.pending_changes

    def test_dislike(self):
        fake_user_id = uuid4()
        tweet = Tweet(uuid4(), "hello", uuid4(), {fake_user_id}, set())

        tweet.dislike(fake_user_id)

        assert fake_user_id not in tweet.liked_user_ids
        assert "liked_user_ids" in tweet.pending_changes

    def test_unretweet(self):
        fake_user_id = uuid4()
        tweet = Tweet(uuid4(), "hello", uuid4(), set(), {fake_user_id})

        tweet.unretweet(fake_user_id)

        assert fake_user_id not in tweet.retweeted_user_ids
        assert "retweeted_user_ids" in tweet.pending_changes
