from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar, final

from botops import telegram

if TYPE_CHECKING:
    from .bot import Bot

__all__ = ["Handler", "MessageHandler", "EditedMessageHandler"]

U = TypeVar(
    "U",
    telegram.Message,
    telegram.CallbackQuery,
    telegram.ChosenInlineResult,
    telegram.ShippingQuery,
    telegram.PreCheckoutQuery,
    telegram.Poll,
    telegram.PollAnswer,
    telegram.ChatJoinRequest,
    telegram.ChatMemberUpdated,
)


class Handler(ABC, Generic[U]):
    __update_type__: telegram.UpdateType

    class Meta:
        propagation: bool = False

    @final
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.update: U | None = None

        if self.Meta is not self.__class__.Meta:

            class _Meta(self.__class__.Meta, self.Meta):
                pass

            self.Meta = _Meta

    @final
    async def __call__(self, update: U) -> None:
        self.update = update
        await self.handle()

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def update_type(self) -> telegram.UpdateType:
        return self.__update_type__

    @abstractmethod
    async def handle(self) -> None:
        pass


class MessageHandler(Handler[telegram.Message], ABC):
    __update_type__: telegram.UpdateType = telegram.UpdateType.message

    async def answer(self, text: str) -> telegram.Message:
        return await self.bot.send_message(chat_id=self.update.chat.id, text=text)


class EditedMessageHandler(MessageHandler, ABC):
    __update_type__: telegram.UpdateType = telegram.UpdateType.edited_message


class PollHandler(Handler[telegram.Poll], ABC):
    __update_type__: telegram.UpdateType = telegram.UpdateType.poll


class PollAnswerHandler(Handler[telegram.PollAnswer], ABC):
    __update_type__: telegram.UpdateType = telegram.UpdateType.poll_answer


class CallbackQueryHandler(Handler[telegram.PollAnswer], ABC):
    __update_type__: telegram.UpdateType = telegram.UpdateType.callback_query


class InlineQueryHandler(Handler[telegram.PollAnswer], ABC):
    __update_type__: telegram.UpdateType = telegram.UpdateType.inline_query
