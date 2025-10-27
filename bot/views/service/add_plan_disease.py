from uuid import UUID

from bot.adapters.ai_health.adapter import AIHealthAdapter
from bot.adapters.ai_health.schemas import AIAAddPlanDiseaseCommand, AIAAddPlanDiseaseResponse

class AddPlanDiseaseView:
    def __init__(self, adapter: AIHealthAdapter):
        self._adapter = adapter

    async def __call__(self, plan_id: UUID, name: str) -> AIAAddPlanDiseaseResponse:

        response = await self._adapter.add_plan_disease(command=AIAAddPlanDiseaseCommand(plan_id=plan_id, name=name))

        return response
