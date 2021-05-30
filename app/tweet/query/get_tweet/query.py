from app.common.query import Query
from uuid import UUID


class GetTweet(Query):
    id: UUID
