from abc import ABC
from app.event.event import IntegrationEvent


class IntegrationEventPublisher(ABC):
    def publish(self, event: IntegrationEvent):
        pass
