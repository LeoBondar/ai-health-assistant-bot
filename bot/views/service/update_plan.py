from uuid import UUID

from bot.adapters.ai_health.adapter import AIHealthAdapter
from bot.adapters.ai_health.schemas import AIAUpdatePlanCommand, AIAUpdatePlanResponse


class UpdatePlanView:
    def __init__(self, adapter: AIHealthAdapter):
        self._adapter = adapter

    async def __call__(self, plan_id: UUID, comment: str) -> AIAUpdatePlanResponse:

        response = await self._adapter.update_plan(command=AIAUpdatePlanCommand(plan_id=plan_id, comment=comment))

        return response