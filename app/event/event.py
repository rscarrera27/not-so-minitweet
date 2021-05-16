from abc import ABC
from app.common.datetime import get_utc_datetime
from datetime import datetime
from uuid import UUID


class Event(ABC):
    occurred_at: datetime

    def __post_init__(self):
        self.occurred_at = get_utc_datetime()


class DomainEvent(Event):
    source_id: UUID
    version: int


class IntegrationEvent(Event):
    pass
