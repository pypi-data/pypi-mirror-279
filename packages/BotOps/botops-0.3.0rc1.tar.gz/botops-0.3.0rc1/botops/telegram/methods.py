from abc import ABC
from typing import Self, TypeVar

from orjson import orjson
from pydantic import BaseModel, ConfigDict, Field, SkipValidation

from .enums import UpdateTypeEnum
from .types import Update, User

__all__ = ("TelegramMethod", "Close", "GetMe", "LogOut", "GetUpdates")

T = TypeVar("T")

R = TypeVar("R")


class TelegramMethod[T](BaseModel, ABC):
    __content_type__: str = "application/json"
    __type__: type[T]

    model_config = ConfigDict(use_enum_values=True, revalidate_instances="never")

    def __call__(self) -> Self:
        return self

    def dump(self) -> bytes:
        """None is incorrect type for telegram API,
        in Telegram Bot API docs Optional means missing field.

        :return: bytes for HTTP request body.
        """

        return orjson.dumps(
            self.model_dump(
                mode="json",
                exclude_unset=True,
                exclude_none=True,
            )
        )


class Close(TelegramMethod[bool]):
    __type__ = bool


class GetMe(TelegramMethod[User]):
    __type__ = User


class LogOut(TelegramMethod[bool]):
    __type__ = bool


class GetUpdates(TelegramMethod[list[Update]]):
    __type__ = list[Update]

    offset: SkipValidation[int | None] = Field(None)
    limit: SkipValidation[int | None] = Field(None)
    timeout: SkipValidation[int | None] = Field(None)
    allowed_updates: SkipValidation[list[UpdateTypeEnum] | None] = Field(None)
