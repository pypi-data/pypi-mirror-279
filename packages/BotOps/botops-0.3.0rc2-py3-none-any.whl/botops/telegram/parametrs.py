from __future__ import annotations

from typing import NotRequired, TypedDict

from botops import telegram

__all__ = ["SendMessage", "GetUpdates"]


class SendMessage(TypedDict):
    chat_id: int
    message_thread_id: NotRequired[int]
    text: NotRequired[str]
    parse_mode: NotRequired[str]
    entities: NotRequired[list[telegram.MessageEntity]]
    disable_web_page_preview: NotRequired[bool]
    disable_notification: NotRequired[bool]
    protect_content: NotRequired[bool]
    reply_to_message_id: NotRequired[int]
    allow_sending_without_reply: NotRequired[bool]
    reply_markup: NotRequired[
        telegram.InlineKeyboardMarkup
        | telegram.ReplyKeyboardMarkup
        | telegram.ReplyKeyboardRemove
        | telegram.ForceReply
    ]


class GetUpdates(TypedDict):
    offset: NotRequired[int]
    limit: NotRequired[int]
    timeout: NotRequired[int]
    allowed_updates: NotRequired[list[telegram.UpdateType]]
