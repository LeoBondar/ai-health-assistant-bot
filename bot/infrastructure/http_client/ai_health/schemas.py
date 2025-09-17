from bot.infrastructure.http_client.models import ApiCamelModel


class AIHCAddChatCommand(ApiCamelModel):
    name: str
    user_id: str


class AIHCGetUserChatCommand(ApiCamelModel):
    limit: int = 10
    offset: int = 0
    user_id: str


class AIHCAddMessageCommand(ApiCamelModel):
    chat_id: str
    user_id: str
    text: str
