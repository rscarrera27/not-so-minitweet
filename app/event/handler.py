from abc import ABC, abstractmethod
from app.event.event import IntegrationEvent
from typing import Generic, TypeVar

ET = TypeVar("ET", bound=IntegrationEvent)


class IntegrationEventHandler(ABC, Generic[ET]):
    @abstractmethod
    async def handle(self, event: ET) -> None:
        pass
