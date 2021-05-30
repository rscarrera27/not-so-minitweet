from app.tweet.domain.model import Tweet, TweetAggregate
from app.tweet.domain.repository import TweetAggregateRepository
from infrastructure.database.tables import TweetTable
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID


class PostgresTweetAggregateRepository(TweetAggregateRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, tweet: TweetAggregate) -> None:
        async with self.session.begin():
            await self.session.execute(TweetTable.insert().values(id=tweet.id, **tweet.pending_changes))

        await self.session.commit()

    async def find_by_id(self, tweet_id: UUID) -> Optional[TweetAggregate]:
        async with self.session.begin():
            query = TweetTable.select().where(TweetTable.c.id == tweet_id)
            result = await self.session.execute(query)
            row = result.fetchone()

        if not row:
            return None

        aggregate = Tweet(
            row["id"], row["text"], row["tweeted_user_id"], set(row["liked_user_ids"]), set(row["retweeted_user_ids"])
        )

        return aggregate
