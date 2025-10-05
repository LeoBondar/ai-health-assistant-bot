from uuid import UUID

from bot.adapters.ai_health.adapter import AIHealthAdapter
from bot.adapters.ai_health.schemas import AIAAddPlanPlaceCommand, AIAAddPlanPlaceResponse


class AddPlanPlaceView:
    def __init__(self, adapter: AIHealthAdapter):
        self._adapter = adapter

    async def __call__(self, plan_id: UUID, place_id: UUID) -> AIAAddPlanPlaceResponse:

        response = await self._adapter.add_plan_place(
            command=AIAAddPlanPlaceCommand(plan_id=plan_id, place_id=place_id)
        )

        return response
