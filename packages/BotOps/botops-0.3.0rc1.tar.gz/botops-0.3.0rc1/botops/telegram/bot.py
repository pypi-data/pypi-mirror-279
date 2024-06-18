from typing import TypeVar

import aiohttp
import orjson

from .erros import TelegramError
from .methods import TelegramMethod
from .types import TelegramResponse

__all__ = ("Bot",)

T = TypeVar("T")


class Bot:
    def __init__(self, token: str, base_url: str = "https://api.telegram.org") -> None:
        self._token = token
        self._id = int(token.split(":")[0])
        self._session = aiohttp.ClientSession(
            base_url=base_url,
        )

    def _construct_url(self, method_url: str) -> str:
        return f"/bot{self._token}/{method_url}"

    async def _request(self, telegram_method: TelegramMethod[T], /) -> TelegramResponse[T]:
        request = self._session.post(
            url=self._construct_url(telegram_method.__class__.__name__),
            data=telegram_method.dump(),
            headers={aiohttp.hdrs.CONTENT_TYPE: telegram_method.__content_type__},
        )

        async with request as response:
            raw_data = await response.json(loads=orjson.loads)
            return TelegramResponse[telegram_method.__type__](**raw_data)

    @property
    def id(self) -> int:
        return self._id

    async def startup(self) -> None:
        pass

    async def shutdown(self) -> None:
        await self._session.close()

    async def exec(self, method: TelegramMethod[T] | type[TelegramMethod[T]], /) -> T:
        response = await self._request(method())

        if not response.ok:
            raise TelegramError(response.error_code, response.description)

        return response.result
