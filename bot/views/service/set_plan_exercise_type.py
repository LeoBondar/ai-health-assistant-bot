from uuid import UUIDfrom uuid import UUID



from bot.adapters.ai_health.adapter import AIHealthAdapterfrom bot.adapters.ai_health.adapter import AIHealthAdapter

from bot.adapters.ai_health.schemas import AIASetPlanExerciseTypeCommand, AIASetPlanExerciseTypeResponsefrom bot.adapters.ai_health.schemas import AIASetPlanExerciseTypeCommand, AIASetPlanExerciseTypeResponse





class SetPlanExerciseTypeView:class SetPlanExerciseTypeView:

    def __init__(self, adapter: AIHealthAdapter):    def __init__(self, adapter: AIHealthAdapter):

        self._adapter = adapter        self._adapter = adapter



    async def __call__(self, plan_id: UUID, exercise_type: str) -> AIASetPlanExerciseTypeResponse:    async def __call__(self, plan_id: UUID, exercise_type: str) -> AIASetPlanExerciseTypeResponse:

        response = await self._adapter.set_plan_exercise_type(        response = await self._adapter.set_plan_exercise_type(

            command=AIASetPlanExerciseTypeCommand(plan_id=plan_id, exercise_type=exercise_type)            command=AIASetPlanExerciseTypeCommand(plan_id=plan_id, exercise_type=exercise_type)

        )        )

        return response
        return response