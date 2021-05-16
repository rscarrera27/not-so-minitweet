from abc import ABC
from app.event.event import IntegrationEvent


class IntegrationEventPublisher(ABC):
    async def publish(self, event: IntegrationEvent) -> None:
        pass
