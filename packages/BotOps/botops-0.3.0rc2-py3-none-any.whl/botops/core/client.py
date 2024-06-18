from dataclasses import dataclass, field
from logging import getLogger
from typing import Any, Literal

import aiohttp

__all__ = ["APIClient", "Response"]

from botops.utils import Cleanup


@dataclass(frozen=True, slots=True, kw_only=True)
class Response:
    ok: bool = field()
    result: list[dict] | dict | bool | None = field(default=None)
    error_code: int | None = field(default=None)
    description: str | None = field(default=None)
    parameters: dict | None = field(default=None)


class APIClient(Cleanup):
    def __init__(self) -> None:
        self._session = aiohttp.ClientSession("https://api.telegram.org")
        self._logger = getLogger(__name__)

    async def _on_startup(self) -> None:
        pass

    async def _on_shutdown(self) -> None:
        self._logger.warning("Closing http session...")
        await self._session.close()

    async def request(self, method: Literal["POST", "GET"], path: str, /, **attrs: Any) -> Response:
        if method == "GET":
            request = self._session.request(method, path, params=self._clear_attrs(attrs))
        else:
            request = self._session.request(method, path, json=self._clear_attrs(attrs))

        async with request as response:
            try:
                raw_data = await response.json()
                return Response(**raw_data)
            except Exception as exc:
                self._logger.error(
                    f"Response status code: {response.status}! {response}", exc_info=exc
                )
                raise

    @staticmethod
    def _clear_attrs(attrs: dict) -> dict:
        for k, v in tuple(attrs.items()):
            if v is None:
                attrs.pop(k, None)
        return attrs
