from uuid import UUID

from bot.adapters.ai_health.adapter import AIHealthAdapter
from bot.adapters.ai_health.schemas import AIADeleteChatCommand, AIADeleteChatResponse

class DeleteChatView:
    def __init__(self, adapter: AIHealthAdapter):
        self._adapter = adapter

    async def __call__(self, chat_id: UUID) -> AIADeleteChatResponse:

        response = await self._adapter.delete_chat(command=AIADeleteChatCommand(chat_id=chat_id))

        return response
