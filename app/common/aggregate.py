from __future__ import annotations

from app.event.event import DomainEvent
from dataclasses import asdict, dataclass, InitVar
from typing import Any, Dict, List
from uuid import UUID

import re


class Aggregate:
    _id: UUID

    @property
    def id(self) -> UUID:
        return self._id


class _EventSourcingFields:
    _version: int
    _pending_events: List[DomainEvent]


@dataclass
class EventSourcedAggregate(Aggregate, _EventSourcingFields):
    aggregate_id: InitVar[UUID]
    aggregate_version: InitVar[int]

    def __post_init__(self, aggregate_id: UUID, aggregate_version: int):
        self._id = aggregate_id
        self._version = aggregate_version
        self._pending_events = []

    @property
    def version(self) -> int:
        return self._version

    @property
    def pending_events(self) -> List[DomainEvent]:
        return self._pending_events

    @staticmethod
    def _camel_to_snake(name):
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    @staticmethod
    def _get_handler_name(event: DomainEvent) -> str:
        event_cls_name = type(event).__name__
        return f"_handle_{EventSourcedAggregate._camel_to_snake(event_cls_name)}"

    def _update(self, event: DomainEvent) -> None:
        event.source_id = self._id
        event.version = self._version + 1

        handler = getattr(self, self._get_handler_name(event))
        handler(event)

        self._version = event.version
        self._pending_events.append(event)


class _DirtyCheckingFields:
    _initial_state: Dict[str, Any]


@dataclass
class DirtyCheckedAggregate(Aggregate, _DirtyCheckingFields):
    aggregate_id: InitVar[UUID]

    def __post_init__(self, aggregate_id: UUID):
        self._id = aggregate_id
        self._initial_state = asdict(self)

    @property
    def pending_changes(self) -> Dict[str, Any]:
        current_state = asdict(self)

        deltas = {k: v for k, v in current_state.items() if (self._initial_state.get(k, "MISSING") != v)}

        return deltas
