from bot.adapters.ai_health.adapter import AIHealthAdapter
from bot.adapters.ai_health.schemas import AIAGetUserGoalsCommand, AIAGetUserGoalsResponse

class GetUserGoalsView:
    def __init__(self, adapter: AIHealthAdapter):
        self._adapter = adapter

    async def __call__(self, limit: int = 10, offset: int = 0) -> AIAGetUserGoalsResponse:

        response = await self._adapter.get_user_goals(command=AIAGetUserGoalsCommand(limit=limit, offset=offset))

        return response
