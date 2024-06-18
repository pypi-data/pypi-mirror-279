from typing import Literal, Required, TypedDict

type MessageAttributes = (
    CallRecordingAttributes
    | ChatAttributes
    | ContactFormAttributes
    | EmailAttributes
    | FacebookMessengerAttributes
    | GenericAttributes
    | PhoneAttributes
    | SmsAttributes
    | TwitterAttributes
    | WhatsAppAttributes
)


class Message(TypedDict, total=False):
    """Message data."""

    id: str
    authorId: str
    externalId: str
    createdAt: str
    attributes: MessageAttributes


class Attachment(TypedDict):
    """Attachment data."""

    prettyName: str
    url: str


type Direction = Literal["Inbound", "Outbound"]


class CallRecordingAttributes(TypedDict, total=False):
    """Call recording attributes."""

    duration: int
    recording: Required[str]
    _type: Literal["CallRecordingAttributes"]


class HtmlContent(TypedDict):
    value: str
    _type: Literal["Html"]


class TextContent(TypedDict):
    value: str
    _type: Literal["Text"]


type Content = HtmlContent | TextContent


class EmailContent(TypedDict):
    """Email content data."""

    content: Content


class EmailContact(TypedDict):
    """Email contact data."""

    email: str
    name: str


class File(TypedDict):
    """File data."""

    prettyName: str
    url: str


class ChatAttributes(TypedDict, total=False):
    attachments: list[Attachment]
    content: Content
    direction: Direction
    isAutomated: Required[bool]
    _type: Literal["ChatAttributes"]


ContactFormAttributes = TypedDict(
    "ContactFormAttributes",
    {
        "attachments": list[Attachment],
        "bcc": list[EmailContact],
        "cc": list[EmailContact],
        "deliveryFailureReason": str,
        "direction": Direction,
        "emailContent": EmailContent,
        "from": EmailContact,
        "inlineImages": list[File],
        "isAutoReply": Required[bool],
        "originalContentUrl": File,
        "replyDefaultToEmails": list[EmailContact],
        "to": list[EmailContact],
        "_type": Literal["ContactFormAttributes"],
    },
    total=False,
)

EmailAttributes = TypedDict(
    "EmailAttributes",
    {
        "attachments": list[Attachment],
        "bcc": list[EmailContact],
        "cc": list[EmailContact],
        "deliveryFailureReason": str,
        "direction": Direction,
        "emailContent": EmailContent,
        "from": Required[EmailContact],
        "inlineImages": list[File],
        "isAutoReply": Required[bool],
        "originalContentUrl": File,
        "replyDefaultToEmails": list[EmailContact],
        "to": list[EmailContact],
        "_type": Literal["EmailAttributes"],
    },
    total=False,
)


class FacebookMessengerAttributes(TypedDict, total=False):
    """Facebook Messenger attributes."""

    attachments: list[Attachment]
    content: Content
    direction: Direction
    _type: Literal["FacebookMessengerAttributes"]


class GenericAttributes(TypedDict, total=False):
    """Generic attributes."""

    attachments: list[Attachment]
    content: Content
    direction: Direction
    _type: Literal["GenericAttributes"]


PhoneAttributes = TypedDict(
    "PhoneAttributes",
    {
        "direction": Direction,
        "duration": int,
        "from": Required[str],
        "to": Required[str],
        "_type": Literal["PhoneAttributes"],
    },
    total=False,
)


class SmsAttributes(TypedDict, total=False):
    """SMS attributes."""

    attachments: list[Attachment]
    content: Content
    direction: Direction
    _type: Literal["SmsAttributes"]


class TwitterAttributes(TypedDict, total=False):
    """Twitter attributes."""

    attachments: list[Attachment]
    content: Content
    direction: Direction
    _type: Literal["TwitterAttributes"]


class WhatsAppAttributes(TypedDict, total=False):
    """WhatsApp attributes."""

    attachments: list[Attachment]
    content: Content
    direction: Direction
    _type: Literal["WhatsAppAttributes"]
