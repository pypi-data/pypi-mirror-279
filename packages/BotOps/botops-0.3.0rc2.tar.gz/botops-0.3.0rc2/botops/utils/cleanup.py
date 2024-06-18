from abc import ABC, abstractmethod
from typing import Any, Self, final

__all__ = ["Cleanup"]


class Cleanup(ABC):
    async def __aenter__(self) -> Self:
        await self.startup()
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.shutdown()

    @abstractmethod
    async def _on_startup(self) -> None:
        pass

    @abstractmethod
    async def _on_shutdown(self) -> None:
        pass

    @final
    async def startup(self) -> None:
        await self._on_startup()

    @final
    async def shutdown(self) -> None:
        await self._on_shutdown()
