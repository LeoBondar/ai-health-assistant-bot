from uuid import UUID

from bot.adapters.ai_health.adapter import AIHealthAdapter
from bot.adapters.ai_health.schemas import AIAAddMessageCommand, AIAAddMessageResponse

class AddChatMessageView:
    def __init__(self, adapter: AIHealthAdapter):
        self._adapter = adapter

    async def __call__(self, user_id: int, chat_id: UUID, text: str) -> AIAAddMessageResponse:

        response = await self._adapter.add_chat_message(
            command=AIAAddMessageCommand(user_id=str(user_id), chat_id=chat_id, text=text)
        )

        return response
