from typing import Any
from urllib.parse import urljoin

from aiohttp import ClientResponse, ClientTimeout, TCPConnector

from bot.infrastructure.http_client.ai_health.schemas import (
    AIHCAddChatCommand,
    AIHCAddMessageCommand,
    AIHCGetUserChatCommand,
)
from bot.infrastructure.http_client.base import BaseHTTPClient
from bot.infrastructure.http_client.enums import RequestMethodType
from bot.settings import settings


class AIHealthHTTPClient(BaseHTTPClient):
    async def add_user_chat(self, command: AIHCAddChatCommand) -> ClientResponse:
        return await self._make_request(
            uri="/api/v1/chats/",
            method=RequestMethodType.POST,
            body=command.model_dump(),
        )

    async def get_user_chat(self, command: AIHCGetUserChatCommand) -> ClientResponse:
        return await self._make_request(
            uri="/api/v1/chats/",
            method=RequestMethodType.GET,
            params={"limit": command.limit, "offset": command.offset, "userId": command.user_id},
        )

    async def add_chat_message(self, command: AIHCAddMessageCommand) -> ClientResponse:
        return await self._make_request(
            uri=f"/api/v1/chats/{command.chat_id}/message",
            method=RequestMethodType.POST,
            body={"text": command.text, "userId": command.user_id},
        )

    async def _make_request(
        self,
        method: RequestMethodType,
        uri: str,
        body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> ClientResponse:
        return await self._request(
            method=method,
            json=body,
            params=params,
            str_or_url=urljoin(settings.ai.base_url, uri),
            ssl=settings.ai.validate_cert,
            timeout=ClientTimeout(total=settings.ai.total_timeout, connect=settings.ai.connect_timeout),
        )

    @staticmethod
    def get_session_config() -> dict[str, Any]:
        return {
            "connector": TCPConnector(limit=settings.ai.connection_limit),
        }
