from bot.adapters.ai_health.adapter import AIHealthAdapter
from bot.adapters.ai_health.schemas import AIAGetRiskFactorsCommand, AIAGetRiskFactorsResponse

class GetRiskFactorsView:
    def __init__(self, adapter: AIHealthAdapter):
        self._adapter = adapter

    async def __call__(self, limit: int = 10, offset: int = 0) -> AIAGetRiskFactorsResponse:

        response = await self._adapter.get_risk_factors(command=AIAGetRiskFactorsCommand(limit=limit, offset=offset))

        return response
