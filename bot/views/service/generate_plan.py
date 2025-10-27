from uuid import UUID

from bot.adapters.ai_health.adapter import AIHealthAdapter
from bot.adapters.ai_health.schemas import AIAGeneratePlanCommand, AIAGeneratePlanResponse

class GeneratePlanView:
    def __init__(self, adapter: AIHealthAdapter):
        self._adapter = adapter

    async def __call__(self, plan_id: UUID) -> AIAGeneratePlanResponse:

        response = await self._adapter.generate_plan(command=AIAGeneratePlanCommand(plan_id=plan_id))

        return response
