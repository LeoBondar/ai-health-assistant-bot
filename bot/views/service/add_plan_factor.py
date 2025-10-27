from uuid import UUID

from bot.adapters.ai_health.adapter import AIHealthAdapter
from bot.adapters.ai_health.schemas import AIAAddPlanFactorCommand, AIAAddPlanFactorResponse

class AddPlanFactorView:
    def __init__(self, adapter: AIHealthAdapter):
        self._adapter = adapter

    async def __call__(self, plan_id: UUID, factor_id: UUID) -> AIAAddPlanFactorResponse:

        response = await self._adapter.add_plan_factor(
            command=AIAAddPlanFactorCommand(plan_id=plan_id, factor_id=factor_id)
        )

        return response
