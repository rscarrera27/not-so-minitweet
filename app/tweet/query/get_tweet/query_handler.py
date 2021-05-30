from app.common.query_handler import QueryHandler
from app.tweet.query.get_tweet.query import GetTweet
from infrastructure.database.tables import TweetTable
from sqlalchemy.ext.asyncio.session import AsyncSession


class GetTweetQueryHandler(QueryHandler[GetTweet, dict]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def handle(self, query: GetTweet) -> dict:
        async with self.session.begin():
            result = await self.session.execute(TweetTable.select().where(TweetTable.c.id == query.id))

        return result.fetchone()
