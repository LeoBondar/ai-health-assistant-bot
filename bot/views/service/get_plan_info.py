from uuid import UUID

from bot.adapters.ai_health.adapter import AIHealthAdapter
from bot.adapters.ai_health.schemas import AIAGetPlanInfoCommand, AIAGetPlanInfoResponse


class GetPlanInfoView:
    def __init__(self, adapter: AIHealthAdapter):
        self._adapter = adapter

    async def __call__(self, plan_id: UUID) -> AIAGetPlanInfoResponse:

        response = await self._adapter.get_plan_info(command=AIAGetPlanInfoCommand(plan_id=plan_id))

        return response
