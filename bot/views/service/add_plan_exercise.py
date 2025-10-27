from uuid import UUID

from bot.adapters.ai_health.adapter import AIHealthAdapter
from bot.adapters.ai_health.schemas import AIAAddPlanExerciseCommand, AIAAddPlanExerciseResponse

class AddPlanExerciseView:
    def __init__(self, adapter: AIHealthAdapter):
        self._adapter = adapter

    async def __call__(self, plan_id: UUID, exercise_id: UUID) -> AIAAddPlanExerciseResponse:

        response = await self._adapter.add_plan_exercise(
            command=AIAAddPlanExerciseCommand(plan_id=plan_id, exercise_id=exercise_id)
        )

        return response
