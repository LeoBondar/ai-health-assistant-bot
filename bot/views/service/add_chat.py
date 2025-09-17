from bot.adapters.ai_health.adapter import AIHealthAdapter
from bot.adapters.ai_health.schemas import AIAAddChatCommand, AIAAddChatResponse


class AddChatView:
    def __init__(self, adapter: AIHealthAdapter):
        self._adapter = adapter

    async def __call__(self, user_id: int, chat_name: str) -> AIAAddChatResponse:

        response = await self._adapter.add_chat(command=AIAAddChatCommand(user_id=str(user_id), name=chat_name))

        return response
