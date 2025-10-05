from uuid import UUID

from bot.adapters.ai_health.adapter import AIHealthAdapter
from bot.adapters.ai_health.schemas import AIAAddPlanGoalCommand, AIAAddPlanGoalResponse


class AddPlanGoalView:
    def __init__(self, adapter: AIHealthAdapter):
        self._adapter = adapter

    async def __call__(self, plan_id: UUID, goal_id: UUID) -> AIAAddPlanGoalResponse:

        response = await self._adapter.add_plan_goal(command=AIAAddPlanGoalCommand(plan_id=plan_id, goal_id=goal_id))

        return response
