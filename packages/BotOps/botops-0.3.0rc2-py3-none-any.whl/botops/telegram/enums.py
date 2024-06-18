from enum import StrEnum, auto

__all__ = ["ChatType", "EntityType", "PollType", "Method", "UpdateType"]


class ChatType(StrEnum):
    private = auto()
    group = auto()
    supergroup = auto()
    channel = auto()


class EntityType(StrEnum):
    mention = auto()
    hashtag = auto()
    cashtag = auto()
    bot_command = auto()
    url = auto()
    email = auto()
    phone_number = auto()
    bold = auto()
    italic = auto()
    underline = auto()
    strikethrough = auto()
    spoiler = auto()
    code = auto()
    pre = auto()
    text_link = auto()
    text_mention = auto()
    custom_emoji = auto()


class PollType(StrEnum):
    regular = auto()
    quiz = auto()


class Method(StrEnum):
    get_me = "getMe"
    log_out = "logOut"
    close = "close"
    send_message = "sendMessage"
    get_updates = "getUpdates"


class UpdateType(StrEnum):
    message = auto()
    edited_message = auto()
    channel_post = auto()
    edited_channel_post = auto()
    inline_query = auto()
    chosen_inline_result = auto()
    callback_query = auto()
    pre_checkout_query = auto()
    poll = auto()
    poll_answer = auto()
    my_chat_member = auto()
    chat_member = auto()
    chat_join_request = auto()
