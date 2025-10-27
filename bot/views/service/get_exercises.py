from bot.adapters.ai_health.adapter import AIHealthAdapter
from bot.adapters.ai_health.schemas import AIAGetExercisesCommand, AIAGetExercisesResponse

class GetExercisesView:
    def __init__(self, adapter: AIHealthAdapter):
        self._adapter = adapter

    async def __call__(self, limit: int = 10, offset: int = 0) -> AIAGetExercisesResponse:

        response = await self._adapter.get_exercises(command=AIAGetExercisesCommand(limit=limit, offset=offset))

        return response
