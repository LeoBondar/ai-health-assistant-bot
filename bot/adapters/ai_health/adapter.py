import json
from typing import Protocol

from bot.adapters.ai_health.schemas import (
    AIAAddChatCommand,
    AIAAddChatResponse,
    AIAAddMessageCommand,
    AIAAddMessageResponse,
    AIAGetUserChatCommand,
    AIAGetUserChatResponse,
)
from bot.infrastructure.http_client.ai_health.client import AIHealthHTTPClient
from bot.infrastructure.http_client.ai_health.schemas import (
    AIHCAddChatCommand,
    AIHCAddMessageCommand,
    AIHCGetUserChatCommand,
)


class IAIHealthAdapter(Protocol):
    async def add_chat(self, command: AIAAddChatCommand) -> AIAAddChatResponse:
        pass

    async def get_chats(self, command: AIAGetUserChatCommand) -> AIAGetUserChatResponse:
        pass

    async def add_chat_message(self, command: AIAAddMessageCommand) -> AIAAddMessageResponse:
        pass


class AIHealthAdapter(IAIHealthAdapter):
    def __init__(self, client: AIHealthHTTPClient):
        self._client = client

    async def get_chats(self, command: AIAGetUserChatCommand) -> AIAGetUserChatResponse:
        response = await self._client.get_user_chat(
            command=AIHCGetUserChatCommand(limit=command.limit, offset=command.offset, user_id=command.user_id)
        )
        body = json.loads(await response.text())
        return AIAGetUserChatResponse(**body["result"])

    async def add_chat_message(self, command: AIAAddMessageCommand) -> AIAAddMessageResponse:
        response = await self._client.add_chat_message(
            command=AIHCAddMessageCommand(chat_id=str(command.chat_id), user_id=command.user_id, text=command.text)
        )
        body = json.loads(await response.text())
        return AIAAddMessageResponse(**body["result"])

    async def add_chat(self, command: AIAAddChatCommand) -> AIAAddChatResponse:
        response = await self._client.add_user_chat(
            command=AIHCAddChatCommand(name=command.name, user_id=command.user_id)
        )
        body = json.loads(await response.text())
        return AIAAddChatResponse(**body["result"])
