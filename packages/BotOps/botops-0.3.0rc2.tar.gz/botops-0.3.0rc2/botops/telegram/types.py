from __future__ import annotations

from attrs import field, frozen

from .enums import ChatType, EntityType, PollType

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
]


@frozen(kw_only=True)
class User:
    id: int = field()
    is_bot: bool = field()
    first_name: str = field()
    last_name: str | None = field(default=None)
    username: str | None = field(default=None)
    language_code: str | None = field(default=None)
    is_premium: bool | None = field(default=None)
    added_to_attachment_menu: bool | None = field(default=None)
    can_join_groups: bool | None = field(default=None)
    can_read_all_group_messages: bool | None = field(default=None)
    supports_inline_queries: bool | None = field(default=None)


@frozen(kw_only=True)
class Chat:
    id: int = field()
    type: ChatType = field()
    title: str | None = field(default=None)
    username: str | None = field(default=None)
    first_name: str | None = field(default=None)
    last_name: str | None = field(default=None)
    is_forum: bool | None = field(default=None)
    photo: ChatPhoto | None = field(default=None)
    active_usernames: list[str] | None = field(default=None)
    emoji_status_custom_emoji_id: str | None = field(default=None)
    emoji_status_expiration_date: int | None = field(default=None)
    bio: str | None = field(default=None)
    has_private_forwards: bool | None = field(default=None)
    has_restricted_voice_and_video_messages: bool | None = field(default=None)
    join_to_send_messages: bool | None = field(default=None)
    join_by_request: bool | None = field(default=None)
    description: str | None = field(default=None)
    invite_link: str | None = field(default=None)
    pinned_message: Message | None = field(default=None)
    permissions: ChatPermissions | None = field(default=None)
    slow_mode_delay: int | None = field(default=None)
    message_auto_delete_time: int | None = field(default=None)
    has_aggressive_anti_spam_enabled: bool | None = field(default=None)
    has_hidden_members: bool | None = field(default=None)
    has_protected_content: bool | None = field(default=None)
    sticker_set_name: str | None = field(default=None)
    can_set_sticker_set: bool | None = field(default=None)
    linked_chat_id: int | None = field(default=None)
    location: ChatLocation | None = field(default=None)


@frozen(kw_only=True)
class Message:
    message_id: int = field()
    message_thread_id: int | None = field(default=None)
    from_user: User | None = field(default=None, metadata={"rename": "from"})
    sender_chat: Chat | None = field(default=None)
    date: int = field()
    chat: Chat = field()
    forward_from: User | None = field(default=None)
    forward_from_chat: Chat | None = field(default=None)
    forward_from_message_id: int | None = field(default=None)
    forward_signature: str | None = field(default=None)
    forward_sender_name: str | None = field(default=None)
    forward_date: int | None = field(default=None)
    is_topic_message: bool | None = field(default=None)
    is_automatic_forward: bool | None = field(default=None)
    reply_to_message: Message | None = field(default=None)
    via_bot: User | None = field(default=None)
    edit_date: int | None = field(default=None)
    has_protected_content: bool | None = field(default=None)
    media_group_id: str | None = field(default=None)
    author_signature: str | None = field(default=None)
    text: str | None = field(default=None)
    entities: list[MessageEntity] | None = field(default=None)
    animation: Animation | None = field(default=None)
    audio: Audio | None = field(default=None)
    document: Document | None = field(default=None)
    photo: list[PhotoSize] | None = field(default=None)
    sticker: Sticker | None = field(default=None)
    story: Story | None = field(default=None)
    video: Video | None = field(default=None)
    video_note: VideoNote | None = field(default=None)
    voice: Voice | None = field(default=None)
    caption: str | None = field(default=None)
    caption_entities: list[MessageEntity] | None = field(default=None)
    has_media_spoiler: bool | None = field(default=None)
    contact: Contact | None = field(default=None)
    dice: Dice | None = field(default=None)
    game: Game | None = field(default=None)
    poll: Poll | None = field(default=None)
    venue: Venue | None = field(default=None)
    location: Location | None = field(default=None)
    new_chat_members: list[User] | None = field(default=None)
    left_chat_member: User | None = field(default=None)
    new_chat_title: str | None = field(default=None)
    new_chat_photo: list[PhotoSize] | None = field(default=None)
    delete_chat_photo: bool | None = field(default=None)
    group_chat_created: bool | None = field(default=None)
    supergroup_chat_created: bool | None = field(default=None)
    channel_chat_created: bool | None = field(default=None)
    message_auto_delete_timer_changed: MessageAutoDeleteTimerChanged | None = field(default=None)
    migrate_to_chat_id: int | None = field(default=None)
    migrate_from_chat_id: int | None = field(default=None)
    pinned_message: Message | None = field(default=None)
    invoice: Invoice | None = field(default=None)
    successful_payment: SuccessfulPayment | None = field(default=None)
    user_shared: UserShared | None = field(default=None)
    chat_shared: ChatShared | None = field(default=None)
    connected_website: str | None = field(default=None)
    write_access_allowed: WriteAccessAllowed | None = field(default=None)
    passport_data: PassportData | None = field(default=None)
    proximity_alert_triggered: ProximityAlertTriggered | None = field(default=None)
    forum_topic_created: ForumTopicCreated | None = field(default=None)
    forum_topic_edited: ForumTopicEdited | None = field(default=None)
    forum_topic_closed: ForumTopicClosed | None = field(default=None)
    forum_topic_reopened: ForumTopicReopened | None = field(default=None)
    general_forum_topic_hidden: GeneralForumTopicHidden | None = field(default=None)
    general_forum_topic_unhidden: GeneralForumTopicUnhidden | None = field(default=None)
    video_chat_scheduled: VideoChatScheduled | None = field(default=None)
    video_chat_started: VideoChatStarted | None = field(default=None)
    video_chat_ended: VideoChatEnded | None = field(default=None)
    video_chat_participants_invited: VideoChatParticipantsInvited | None = field(default=None)
    web_app_data: WebAppData | None = field(default=None)
    reply_markup: InlineKeyboardMarkup | None = field(default=None)


@frozen(kw_only=True)
class MessageId:
    message_id: int = field()


@frozen(kw_only=True)
class MessageEntity:
    type: EntityType = field()
    offset: int = field()
    length: int = field()
    url: str | None = field(default=None)
    user: User | None = field(default=None)
    language: str | None = field(default=None)
    custom_emoji_id: str | None = field(default=None)


@frozen(kw_only=True)
class PhotoSize:
    file_id: str = field()
    file_unique_id: str = field()
    width: int = field()
    height: int = field()
    file_size: int | None = field(default=None)


@frozen(kw_only=True)
class Animation:
    file_id: str = field()
    file_unique_id: str = field()
    width: int = field()
    height: int = field()
    duration: int = field()
    thumbnail: PhotoSize | None = field(default=None)
    file_name: str | None = field(default=None)
    mime_type: str | None = field(default=None)
    file_size: int | None = field(default=None)


@frozen(kw_only=True)
class Audio:
    file_id: str = field()
    file_unique_id: str = field()
    duration: int = field()
    performer: str | None = field(default=None)
    title: str | None = field(default=None)
    file_name: str | None = field(default=None)
    mime_type: str | None = field(default=None)
    file_size: int | None = field(default=None)
    thumbnail: PhotoSize | None = field(default=None)


@frozen(kw_only=True)
class Document:
    file_id: str = field()
    file_unique_id: str = field()
    thumbnail: PhotoSize | None = field(default=None)
    file_name: str | None = field(default=None)
    mime_type: str | None = field(default=None)
    file_size: int | None = field(default=None)


@frozen(kw_only=True)
class Story:
    ...


@frozen(kw_only=True)
class Video:
    file_id: str = field()
    file_unique_id: str = field()
    width: int = field()
    height: int = field()
    duration: int = field()
    thumbnail: PhotoSize | None = field(default=None)
    file_name: str | None = field(default=None)
    mime_type: str | None = field(default=None)
    file_size: int | None = field(default=None)


@frozen(kw_only=True)
class VideoNote:
    file_id: str = field()
    file_unique_id: str = field()
    length: int = field()
    duration: int = field()
    thumbnail: PhotoSize | None = field(default=None)
    file_size: int | None = field(default=None)


@frozen(kw_only=True)
class Voice:
    file_id: str = field()
    file_unique_id: str = field()
    duration: int = field()
    mime_type: str | None = field(default=None)
    file_size: int | None = field(default=None)


@frozen(kw_only=True)
class Contact:
    phone_number: str = field()
    first_name: str = field()
    last_name: str | None = field(default=None)
    user_id: int | None = field(default=None)
    vcard: str | None = field(default=None)


@frozen(kw_only=True)
class Dice:
    emoji: str = field()
    value: int = field()


@frozen(kw_only=True)
class PollOption:
    text: str = field()
    voter_count: int = field()


@frozen(kw_only=True)
class PollAnswer:
    poll_id: str = field()
    voter_chat: Chat | None = field(default=None)
    user: User | None = field(default=None)
    option_ids: list[int] = field()


@frozen(kw_only=True)
class Poll:
    id: str = field()
    question: str = field()
    options: list[PollOption] = field()
    total_voter_count: int = field()
    is_closed: bool = field()
    is_anonymous: bool = field()
    type: PollType = field()
    allows_multiple_answers: bool = field()
    correct_option_id: int | None = field(default=None)
    explanation: str | None = field(default=None)
    explanation_entities: list[MessageEntity] | None = field(default=None)
    open_period: int | None = field(default=None)
    close_date: int | None = field(default=None)


@frozen(kw_only=True)
class Location:
    longitude: float = field()
    latitude: float = field()
    horizontal_accuracy: float | None = field(default=None)
    live_period: int | None = field(default=None)
    heading: int | None = field(default=None)
    proximity_alert_radius: int | None = field(default=None)


@frozen(kw_only=True)
class Venue:
    location: Location = field()
    title: str = field()
    address: str = field()
    foursquare_id: str | None = field(default=None)
    foursquare_type: str | None = field(default=None)
    google_place_id: str | None = field(default=None)
    google_place_type: str | None = field(default=None)


@frozen(kw_only=True)
class WebAppData:
    data: str = field()
    button_text: str = field()


@frozen(kw_only=True)
class ProximityAlertTriggered:
    ...


@frozen(kw_only=True)
class MessageAutoDeleteTimerChanged:
    ...


@frozen(kw_only=True)
class ForumTopicCreated:
    ...


@frozen(kw_only=True)
class ForumTopicClosed:
    ...


@frozen(kw_only=True)
class ForumTopicReopened:
    ...


@frozen(kw_only=True)
class GeneralForumTopicHidden:
    ...


@frozen(kw_only=True)
class UserShared:
    ...


@frozen(kw_only=True)
class ChatShared:
    ...


@frozen(kw_only=True)
class WriteAccessAllowed:
    ...


@frozen(kw_only=True)
class VideoChatScheduled:
    ...


@frozen(kw_only=True)
class VideoChatStarted:
    ...


@frozen(kw_only=True)
class VideoChatEnded:
    ...


@frozen(kw_only=True)
class VideoChatParticipantsInvited:
    ...


@frozen(kw_only=True)
class UserProfilePhotos:
    ...


@frozen(kw_only=True)
class File:
    ...


@frozen(kw_only=True)
class ChatPhoto:
    small_file_id: str = field()
    small_file_unique_id: str = field()
    big_file_id: str = field()
    big_file_unique_id: str = field()


@frozen(kw_only=True)
class ChatPermissions:
    can_send_messages: bool | None = field(default=None)
    can_send_audios: bool | None = field(default=None)
    can_send_documents: bool | None = field(default=None)
    can_send_photos: bool | None = field(default=None)
    can_send_videos: bool | None = field(default=None)
    can_send_video_notes: bool | None = field(default=None)
    can_send_voice_notes: bool | None = field(default=None)
    can_send_polls: bool | None = field(default=None)
    can_send_other_messages: bool | None = field(default=None)
    can_add_web_page_previews: bool | None = field(default=None)
    can_change_info: bool | None = field(default=None)
    can_invite_users: bool | None = field(default=None)
    can_pin_messages: bool | None = field(default=None)
    can_manage_topics: bool | None = field(default=None)


@frozen(kw_only=True)
class ChatLocation:
    location: Location = field()
    address: str = field()


@frozen(kw_only=True)
class Sticker:
    ...


@frozen(kw_only=True)
class Game:
    ...


@frozen(kw_only=True)
class SuccessfulPayment:
    ...


@frozen(kw_only=True)
class PassportData:
    ...


@frozen(kw_only=True)
class ForumTopicEdited:
    ...


@frozen(kw_only=True)
class GeneralForumTopicUnhidden:
    ...


@frozen(kw_only=True)
class InlineKeyboardMarkup:
    ...


@frozen(kw_only=True)
class ReplyKeyboardMarkup:
    ...


@frozen(kw_only=True)
class ReplyKeyboardRemove:
    ...


@frozen(kw_only=True)
class ForceReply:
    ...


@frozen(kw_only=True)
class InlineQuery:
    ...


@frozen(kw_only=True)
class ChosenInlineResult:
    ...


@frozen(kw_only=True)
class CallbackQuery:
    ...


@frozen(kw_only=True)
class ShippingQuery:
    ...


@frozen(kw_only=True)
class PreCheckoutQuery:
    ...


@frozen(kw_only=True)
class ChatMemberUpdated:
    ...


@frozen(kw_only=True)
class ChatJoinRequest:
    ...


@frozen(kw_only=True)
class Invoice:
    title: str = field()
    description: str = field()
    start_parameter: str = field()
    currency: str = field()
    total_amount: float = field()


@frozen(kw_only=True)
class Update:
    update_id: int = field()
    message: Message | None = field(default=None)
    edited_message: Message | None = field(default=None)
    channel_post: Message | None = field(default=None)
    edited_channel_post: Message | None = field(default=None)
    inline_query: InlineQuery | None = field(default=None)
    chosen_inline_result: ChosenInlineResult | None = field(default=None)
    callback_query: CallbackQuery | None = field(default=None)
    shipping_query: ShippingQuery | None = field(default=None)
    pre_checkout_query: PreCheckoutQuery | None = field(default=None)
    poll: Poll | None = field(default=None)
    poll_answer: PollAnswer | None = field(default=None)
    my_chat_member: ChatMemberUpdated | None = field(default=None)
    chat_member: ChatMemberUpdated | None = field(default=None)
    chat_join_request: ChatJoinRequest | None = field(default=None)
