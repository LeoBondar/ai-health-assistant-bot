from bot.adapters.ai_health.adapter import AIHealthAdapter
from bot.adapters.ai_health.schemas import AIAGetUserChatCommand, AIAGetUserChatResponse

class GetUserChatsView:
    def __init__(self, adapter: AIHealthAdapter):
        self._adapter = adapter

    async def __call__(self, user_id: int) -> AIAGetUserChatResponse:

        response = await self._adapter.get_chats(command=AIAGetUserChatCommand(user_id=str(user_id)))

        return response
