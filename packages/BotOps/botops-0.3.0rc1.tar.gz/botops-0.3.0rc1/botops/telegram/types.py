from __future__ import annotations

from abc import ABC

from pydantic import BaseModel, ConfigDict, Field, SkipValidation

from botops.telegram.enums import EntityTypeEnum, PollTypeEnum

__all__ = [
    "Update",
    "User",
    "Message",
    "CallbackQuery",
    "InlineQuery",
    "ReplyKeyboardRemove",
    "InlineKeyboardMarkup",
    "ForceReply",
    "MessageEntity",
    "ReplyKeyboardMarkup",
    "ChosenInlineResult",
    "ShippingQuery",
    "PreCheckoutQuery",
    "Poll",
    "PollAnswer",
    "ChatJoinRequest",
    "ChatMemberUpdated",
    "TelegramType",
    "TelegramResponse",
]


class TelegramType(BaseModel, ABC):
    model_config = ConfigDict(
        frozen=True, populate_by_name=True, use_enum_values=True, revalidate_instances="never"
    )


class TelegramResponse[R](TelegramType):
    ok: SkipValidation[bool] = Field()
    result: R | None = Field(default=None)
    error_code: SkipValidation[int | None] = Field(default=None)
    description: SkipValidation[str | None] = Field(default=None)
    parameters: SkipValidation[dict | None] = Field(default=None)


class User(TelegramType):
    id: int = Field()
    is_bot: bool = Field()
    first_name: str = Field()
    last_name: str | None = Field(default=None)
    username: str | None = Field(default=None)
    language_code: str | None = Field(default=None)
    is_premium: bool | None = Field(default=None)
    added_to_attachment_menu: bool | None = Field(default=None)
    can_join_groups: bool | None = Field(default=None)
    can_read_all_group_messages: bool | None = Field(default=None)
    supports_inline_queries: bool | None = Field(default=None)


class Chat(TelegramType):
    id: int = Field()
    type: Chat = Field()
    title: str | None = Field(default=None)
    username: str | None = Field(default=None)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    is_forum: bool | None = Field(default=None)
    photo: ChatPhoto | None = Field(default=None)
    active_usernames: list[str] | None = Field(default=None)
    emoji_status_custom_emoji_id: str | None = Field(default=None)
    emoji_status_expiration_date: int | None = Field(default=None)
    bio: str | None = Field(default=None)
    has_private_forwards: bool | None = Field(default=None)
    has_restricted_voice_and_video_messages: bool | None = Field(default=None)
    join_to_send_messages: bool | None = Field(default=None)
    join_by_request: bool | None = Field(default=None)
    description: str | None = Field(default=None)
    invite_link: str | None = Field(default=None)
    pinned_message: Message | None = Field(default=None)
    permissions: ChatPermissions | None = Field(default=None)
    slow_mode_delay: int | None = Field(default=None)
    message_auto_delete_time: int | None = Field(default=None)
    has_aggressive_anti_spam_enabled: bool | None = Field(default=None)
    has_hidden_members: bool | None = Field(default=None)
    has_protected_content: bool | None = Field(default=None)
    sticker_set_name: str | None = Field(default=None)
    can_set_sticker_set: bool | None = Field(default=None)
    linked_chat_id: int | None = Field(default=None)
    location: ChatLocation | None = Field(default=None)


class Message(TelegramType):
    message_id: int = Field()
    message_thread_id: int | None = Field(default=None)
    from_user: User | None = Field(default=None, alias="from")
    sender_chat: Chat | None = Field(default=None)
    date: int = Field()
    chat: Chat = Field()
    forward_from: User | None = Field(default=None)
    forward_from_chat: Chat | None = Field(default=None)
    forward_from_message_id: int | None = Field(default=None)
    forward_signature: str | None = Field(default=None)
    forward_sender_name: str | None = Field(default=None)
    forward_date: int | None = Field(default=None)
    is_topic_message: bool | None = Field(default=None)
    is_automatic_forward: bool | None = Field(default=None)
    reply_to_message: Message | None = Field(default=None)
    via_bot: User | None = Field(default=None)
    edit_date: int | None = Field(default=None)
    has_protected_content: bool | None = Field(default=None)
    media_group_id: str | None = Field(default=None)
    author_signature: str | None = Field(default=None)
    text: str | None = Field(default=None)
    entities: list[MessageEntity] | None = Field(default=None)
    animation: Animation | None = Field(default=None)
    audio: Audio | None = Field(default=None)
    document: Document | None = Field(default=None)
    photo: list[PhotoSize] | None = Field(default=None)
    sticker: Sticker | None = Field(default=None)
    story: Story | None = Field(default=None)
    video: Video | None = Field(default=None)
    video_note: VideoNote | None = Field(default=None)
    voice: Voice | None = Field(default=None)
    caption: str | None = Field(default=None)
    caption_entities: list[MessageEntity] | None = Field(default=None)
    has_media_spoiler: bool | None = Field(default=None)
    contact: Contact | None = Field(default=None)
    dice: Dice | None = Field(default=None)
    game: Game | None = Field(default=None)
    poll: Poll | None = Field(default=None)
    venue: Venue | None = Field(default=None)
    location: Location | None = Field(default=None)
    new_chat_members: list[User] | None = Field(default=None)
    left_chat_member: User | None = Field(default=None)
    new_chat_title: str | None = Field(default=None)
    new_chat_photo: list[PhotoSize] | None = Field(default=None)
    delete_chat_photo: bool | None = Field(default=None)
    group_chat_created: bool | None = Field(default=None)
    supergroup_chat_created: bool | None = Field(default=None)
    channel_chat_created: bool | None = Field(default=None)
    message_auto_delete_timer_changed: MessageAutoDeleteTimerChanged | None = Field(default=None)
    migrate_to_chat_id: int | None = Field(default=None)
    migrate_from_chat_id: int | None = Field(default=None)
    pinned_message: Message | None = Field(default=None)
    invoice: Invoice | None = Field(default=None)
    successful_payment: SuccessfulPayment | None = Field(default=None)
    user_shared: UserShared | None = Field(default=None)
    chat_shared: ChatShared | None = Field(default=None)
    connected_website: str | None = Field(default=None)
    write_access_allowed: WriteAccessAllowed | None = Field(default=None)
    passport_data: PassportData | None = Field(default=None)
    proximity_alert_triggered: ProximityAlertTriggered | None = Field(default=None)
    forum_topic_created: ForumTopicCreated | None = Field(default=None)
    forum_topic_edited: ForumTopicEdited | None = Field(default=None)
    forum_topic_closed: ForumTopicClosed | None = Field(default=None)
    forum_topic_reopened: ForumTopicReopened | None = Field(default=None)
    general_forum_topic_hidden: GeneralForumTopicHidden | None = Field(default=None)
    general_forum_topic_unhidden: GeneralForumTopicUnhidden | None = Field(default=None)
    video_chat_scheduled: VideoChatScheduled | None = Field(default=None)
    video_chat_started: VideoChatStarted | None = Field(default=None)
    video_chat_ended: VideoChatEnded | None = Field(default=None)
    video_chat_participants_invited: VideoChatParticipantsInvited | None = Field(default=None)
    web_app_data: WebAppData | None = Field(default=None)
    reply_markup: InlineKeyboardMarkup | None = Field(default=None)


class MessageId(TelegramType):
    message_id: int = Field()


class MessageEntity(TelegramType):
    type: EntityTypeEnum = Field()
    offset: int = Field()
    length: int = Field()
    url: str | None = Field(default=None)
    user: User | None = Field(default=None)
    language: str | None = Field(default=None)
    custom_emoji_id: str | None = Field(default=None)


class PhotoSize(TelegramType):
    file_id: str = Field()
    file_unique_id: str = Field()
    width: int = Field()
    height: int = Field()
    file_size: int | None = Field(default=None)


class Animation(TelegramType):
    file_id: str = Field()
    file_unique_id: str = Field()
    width: int = Field()
    height: int = Field()
    duration: int = Field()
    thumbnail: PhotoSize | None = Field(default=None)
    file_name: str | None = Field(default=None)
    mime_type: str | None = Field(default=None)
    file_size: int | None = Field(default=None)


class Audio(TelegramType):
    file_id: str = Field()
    file_unique_id: str = Field()
    duration: int = Field()
    performer: str | None = Field(default=None)
    title: str | None = Field(default=None)
    file_name: str | None = Field(default=None)
    mime_type: str | None = Field(default=None)
    file_size: int | None = Field(default=None)
    thumbnail: PhotoSize | None = Field(default=None)


class Document(TelegramType):
    file_id: str = Field()
    file_unique_id: str = Field()
    thumbnail: PhotoSize | None = Field(default=None)
    file_name: str | None = Field(default=None)
    mime_type: str | None = Field(default=None)
    file_size: int | None = Field(default=None)


class Story(TelegramType): ...


class Video(TelegramType):
    file_id: str = Field()
    file_unique_id: str = Field()
    width: int = Field()
    height: int = Field()
    duration: int = Field()
    thumbnail: PhotoSize | None = Field(default=None)
    file_name: str | None = Field(default=None)
    mime_type: str | None = Field(default=None)
    file_size: int | None = Field(default=None)


class VideoNote(TelegramType):
    file_id: str = Field()
    file_unique_id: str = Field()
    length: int = Field()
    duration: int = Field()
    thumbnail: PhotoSize | None = Field(default=None)
    file_size: int | None = Field(default=None)


class Voice(TelegramType):
    file_id: str = Field()
    file_unique_id: str = Field()
    duration: int = Field()
    mime_type: str | None = Field(default=None)
    file_size: int | None = Field(default=None)


class Contact(TelegramType):
    phone_number: str = Field()
    first_name: str = Field()
    last_name: str | None = Field(default=None)
    user_id: int | None = Field(default=None)
    vcard: str | None = Field(default=None)


class Dice(TelegramType):
    emoji: str = Field()
    value: int = Field()


class PollOption(TelegramType):
    text: str = Field()
    voter_count: int = Field()


class PollAnswer(TelegramType):
    poll_id: str = Field()
    voter_chat: Chat | None = Field(default=None)
    user: User | None = Field(default=None)
    option_ids: list[int] = Field()


class Poll(TelegramType):
    id: str = Field()
    question: str = Field()
    options: list[PollOption] = Field()
    total_voter_count: int = Field()
    is_closed: bool = Field()
    is_anonymous: bool = Field()
    type: PollTypeEnum = Field()
    allows_multiple_answers: bool = Field()
    correct_option_id: int | None = Field(default=None)
    explanation: str | None = Field(default=None)
    explanation_entities: list[MessageEntity] | None = Field(default=None)
    open_period: int | None = Field(default=None)
    close_date: int | None = Field(default=None)


class Location(TelegramType):
    longitude: float = Field()
    latitude: float = Field()
    horizontal_accuracy: float | None = Field(default=None)
    live_period: int | None = Field(default=None)
    heading: int | None = Field(default=None)
    proximity_alert_radius: int | None = Field(default=None)


class Venue(TelegramType):
    location: Location = Field()
    title: str = Field()
    address: str = Field()
    foursquare_id: str | None = Field(default=None)
    foursquare_type: str | None = Field(default=None)
    google_place_id: str | None = Field(default=None)
    google_place_type: str | None = Field(default=None)


class WebAppData(TelegramType):
    data: str = Field()
    button_text: str = Field()


class ProximityAlertTriggered(TelegramType): ...


class MessageAutoDeleteTimerChanged(TelegramType): ...


class ForumTopicCreated(TelegramType): ...


class ForumTopicClosed(TelegramType): ...


class ForumTopicReopened(TelegramType): ...


class GeneralForumTopicHidden(TelegramType): ...


class UserShared(TelegramType): ...


class ChatShared(TelegramType): ...


class WriteAccessAllowed(TelegramType): ...


class VideoChatScheduled(TelegramType): ...


class VideoChatStarted(TelegramType): ...


class VideoChatEnded(TelegramType): ...


class VideoChatParticipantsInvited(TelegramType): ...


class UserProfilePhotos(TelegramType): ...


class File(TelegramType): ...


class ChatPhoto(TelegramType):
    small_file_id: str = Field()
    small_file_unique_id: str = Field()
    big_file_id: str = Field()
    big_file_unique_id: str = Field()


class ChatPermissions(TelegramType):
    can_send_messages: bool | None = Field(default=None)
    can_send_audios: bool | None = Field(default=None)
    can_send_documents: bool | None = Field(default=None)
    can_send_photos: bool | None = Field(default=None)
    can_send_videos: bool | None = Field(default=None)
    can_send_video_notes: bool | None = Field(default=None)
    can_send_voice_notes: bool | None = Field(default=None)
    can_send_polls: bool | None = Field(default=None)
    can_send_other_messages: bool | None = Field(default=None)
    can_add_web_page_previews: bool | None = Field(default=None)
    can_change_info: bool | None = Field(default=None)
    can_invite_users: bool | None = Field(default=None)
    can_pin_messages: bool | None = Field(default=None)
    can_manage_topics: bool | None = Field(default=None)


class ChatLocation(TelegramType):
    location: Location = Field()
    address: str = Field()


class Sticker(TelegramType): ...


class Game(TelegramType): ...


class SuccessfulPayment(TelegramType): ...


class PassportData(TelegramType): ...


class ForumTopicEdited(TelegramType): ...


class GeneralForumTopicUnhidden(TelegramType): ...


class InlineKeyboardMarkup(TelegramType): ...


class ReplyKeyboardMarkup(TelegramType): ...


class ReplyKeyboardRemove(TelegramType): ...


class ForceReply(TelegramType): ...


class InlineQuery(TelegramType): ...


class ChosenInlineResult(TelegramType): ...


class CallbackQuery(TelegramType): ...


class ShippingQuery(TelegramType): ...


class PreCheckoutQuery(TelegramType): ...


class ChatMemberUpdated(TelegramType): ...


class ChatJoinRequest(TelegramType): ...


class Invoice(TelegramType):
    title: str = Field()
    description: str = Field()
    start_parameter: str = Field()
    currency: str = Field()
    total_amount: float = Field()


class Update(TelegramType):
    update_id: int = Field()
    message: Message | None = Field(default=None)
    edited_message: Message | None = Field(default=None)
    channel_post: Message | None = Field(default=None)
    edited_channel_post: Message | None = Field(default=None)
    inline_query: InlineQuery | None = Field(default=None)
    chosen_inline_result: ChosenInlineResult | None = Field(default=None)
    callback_query: CallbackQuery | None = Field(default=None)
    shipping_query: ShippingQuery | None = Field(default=None)
    pre_checkout_query: PreCheckoutQuery | None = Field(default=None)
    poll: Poll | None = Field(default=None)
    poll_answer: PollAnswer | None = Field(default=None)
    my_chat_member: ChatMemberUpdated | None = Field(default=None)
    chat_member: ChatMemberUpdated | None = Field(default=None)
    chat_join_request: ChatJoinRequest | None = Field(default=None)
