from uuid import UUID

from bot.infrastructure.http_client.models import ApiCamelModel


class AIAAddChatCommand(ApiCamelModel):
    name: str
    user_id: str


class AIAGetUserChatCommand(ApiCamelModel):
    limit: int = 10
    offset: int = 0
    user_id: str


class AIAAddMessageCommand(ApiCamelModel):
    chat_id: UUID
    user_id: str
    text: str


class AIAAddChatResponse(ApiCamelModel):
    id: UUID


class ChatInfo(ApiCamelModel):
    id: UUID
    name: str


class AIAGetUserChatResponse(ApiCamelModel):
    chats: list[ChatInfo] | None


class AIAAddMessageResponse(ApiCamelModel):
    text: str
