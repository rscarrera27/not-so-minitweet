from app.common.datetime import get_utc_datetime
from app.user.domain.event import (
    BioUpdated,
    FollowedUser,
    PasswordChanged,
    UnfollowedUser,
    UserLoggedIn,
    UsernameUpdated,
)
from app.user.domain.model import User, UserCredential
from uuid import uuid4

import pytest


class UserCredentialStub(UserCredential):
    def __init__(self, verify_return):
        self.verify_return = verify_return

    @staticmethod
    def hash(new_password: str) -> UserCredential:
        pass

    def verify(self, password: str) -> bool:
        return self.verify_return


class TestUserAggregate:
    @pytest.fixture
    def user(self):
        return User(
            aggregate_id=uuid4(),
            aggregate_version=0,
            screen_id="a",
            username="a",
            bio=None,
            following=set(),
            credential=UserCredentialStub(verify_return=True),
            last_login=get_utc_datetime(),
        )

    class TestLogin:
        def test_with_valid_password(self):
            last_login = get_utc_datetime()
            user = User(
                aggregate_id=uuid4(),
                aggregate_version=0,
                screen_id="a",
                username="a",
                bio=None,
                following=set(),
                credential=UserCredentialStub(verify_return=True),
                last_login=last_login,
            )

            user.login("password")

            assert user.last_login != last_login
            assert isinstance(user.pending_events.pop(), UserLoggedIn)

        def test_with_invalid_password(self):
            last_login = get_utc_datetime()
            user = User(
                aggregate_id=uuid4(),
                aggregate_version=0,
                screen_id="a",
                username="a",
                bio=None,
                following=set(),
                credential=UserCredentialStub(verify_return=False),
                last_login=last_login,
            )

            with pytest.raises(ValueError):
                user.login("password")

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

    class TestChangePassword:
        def test_when_password_verification_succeed(self, user):
            new_cred = UserCredentialStub(verify_return=True)
            user.change_password("old_pw", new_cred)

            assert user.credential == new_cred
            assert isinstance(user.pending_events.pop(), PasswordChanged)

        def test_when_password_verification_failed(self, user):
            user.credential = UserCredentialStub(verify_return=False)

            with pytest.raises(ValueError):
                user.change_password("wrong_pw", UserCredentialStub(verify_return=True))

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
