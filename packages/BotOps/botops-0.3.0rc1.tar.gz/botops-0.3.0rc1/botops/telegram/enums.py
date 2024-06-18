from enum import StrEnum, auto

__all__ = ("ChatTypeEnum", "EntityTypeEnum", "PollTypeEnum", "UpdateTypeEnum")


class ChatTypeEnum(StrEnum):
    private = auto()
    group = auto()
    supergroup = auto()
    channel = auto()


class EntityTypeEnum(StrEnum):
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


class PollTypeEnum(StrEnum):
    regular = auto()
    quiz = auto()


class UpdateTypeEnum(StrEnum):
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
