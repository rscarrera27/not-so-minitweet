from app.tweet.adapters.repository import PostgresTweetAggregateRepository
from app.tweet.domain.model import Tweet
from uuid import uuid4

import pytest


class TestSave:
    @pytest.mark.asyncio
    async def test_save(self, postgres_session):
        repo = PostgresTweetAggregateRepository(postgres_session)
        aggregate = Tweet.new("Hello", uuid4())

        await repo.save(aggregate)

        print(await repo.find_by_id(aggregate.id))


class TestFindById:
    @pytest.mark.asyncio
    async def test_not_found(self, postgres_session):
        repo = PostgresTweetAggregateRepository(postgres_session)

        result = await repo.find_by_id(uuid4())
        assert result is None
