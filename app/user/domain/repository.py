from abc import ABC, abstractmethod
from app.user.domain.model import UserAggregate
from uuid import UUID


class UserAggregateRepository(ABC):
    @abstractmethod
    async def save(self, user: UserAggregate):
        pass

    @abstractmethod
    async def find_by_id(self, aggregate_id: UUID) -> UserAggregate:
        pass
