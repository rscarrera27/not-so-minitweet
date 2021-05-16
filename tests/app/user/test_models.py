from app.user.domain.event import (
    BioUpdated,
    FollowedUser,
    UnfollowedUser,
    UsernameUpdated,
)
from app.user.domain.model import User
from uuid import uuid4

import pytest


class TestUserAggregate:
    @pytest.fixture
    def user(self):
        return User(aggregate_id=uuid4(), aggregate_version=0, screen_id="a", username="a", bio=None, following=set())

    class TestUpdateUsername:
        def test_with_valid_username(self, user):
            user.update_username("b")

            assert user.username == "b"
            assert isinstance(user.pending_events.pop(), UsernameUpdated)

        def test_with_too_long_username(self, user):
            with pytest.raises(ValueError):
                user.update_username("x" * 10)

    class TestUpdateBio:
        def test_with_valid_bio(self, user):
            user.update_bio("hello world")

            assert user.bio == "hello world"
            assert isinstance(user.pending_events.pop(), BioUpdated)

        def test_with_too_long_bio(self, user):
            with pytest.raises(ValueError):
                user.update_bio("x" * 200)

    class TestFollowUser:
        def test_follow_user(self, user):
            fake_user_id = uuid4()
            user.follow_user(fake_user_id)

            assert fake_user_id in user.following
            assert isinstance(user.pending_events.pop(), FollowedUser)

    class TestUnfollowUser:
        def test_unfollow_user(self, user):
            fake_user_id = uuid4()
            user.following = {fake_user_id}

            user.unfollow_user(fake_user_id)

            assert fake_user_id not in user.following
            assert isinstance(user.pending_events.pop(), UnfollowedUser)
