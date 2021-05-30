from abc import ABC, abstractmethod
from app.common.query import Query
from typing import Generic, TypeVar

QT = TypeVar("QT", bound=Query)
RT = TypeVar("RT")


class QueryHandler(ABC, Generic[QT, RT]):
    @abstractmethod
    async def handle(self, query: QT) -> RT:
        pass
