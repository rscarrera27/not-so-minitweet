from abc import ABC, abstractmethod
from app.common.command import Command
from typing import Generic, TypeVar

CT = TypeVar("CT", bound=Command)


class CommandHandler(ABC, Generic[CT]):
    @abstractmethod
    async def handle(self, command: CT) -> None:
        pass
