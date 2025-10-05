from bot.adapters.ai_health.adapter import AIHealthAdapter
from bot.adapters.ai_health.schemas import AIAGetPlacesCommand, AIAGetPlacesResponse


class GetPlacesView:
    def __init__(self, adapter: AIHealthAdapter):
        self._adapter = adapter

    async def __call__(self, limit: int = 10, offset: int = 0) -> AIAGetPlacesResponse:

        response = await self._adapter.get_places(command=AIAGetPlacesCommand(limit=limit, offset=offset))

        return response
