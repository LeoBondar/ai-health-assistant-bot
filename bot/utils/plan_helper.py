from typing import Optional
from uuid import UUID

from bot.adapters.ai_health.schemas import AIAGetPlanInfoResponse
from bot.fsm.states import PlanFillingStates

class PlanFillingHelper:

    @staticmethod
    def get_next_step(plan_info: AIAGetPlanInfoResponse) -> Optional[str]:

        if plan_info.risk_factor is None:
            return PlanFillingStates.choosing_factor.state

        if plan_info.disease is None:
            return PlanFillingStates.entering_disease.state

        if plan_info.user_goal is None:
            return PlanFillingStates.choosing_goal.state

        if plan_info.place is None:
            return PlanFillingStates.choosing_place.state

        if plan_info.exercise is None:
            return PlanFillingStates.choosing_exercise.state
            
        if plan_info.exercise_type is None:
            return PlanFillingStates.choosing_exercise_type.state

        return PlanFillingStates.plan_completed.state

    @staticmethod
    def is_plan_complete(plan_info: AIAGetPlanInfoResponse) -> bool:

        return (
            plan_info.risk_factor is not None
            and plan_info.disease is not None
            and plan_info.user_goal is not None
            and plan_info.place is not None
            and plan_info.exercise is not None
            and plan_info.exercise_type is not None
        )

    @staticmethod
    def format_plan_info(plan_info: AIAGetPlanInfoResponse) -> str:

        lines = []

        if plan_info.risk_factor:
            lines.append(f"🔍 Risk Factor: {plan_info.risk_factor.factor}")
        else:
            lines.append("🔍 Risk Factor: not filled")

        if plan_info.disease:
            lines.append(f"🏥 Disease: {plan_info.disease.name}")
        else:
            lines.append("🏥 Disease: not filled")

        if plan_info.user_goal:
            lines.append(f"🎯 Goal: {plan_info.user_goal.name}")
        else:
            lines.append("🎯 Goal: not filled")

        if plan_info.place:
            lines.append(f"📍 Place: {plan_info.place.name}")
        else:
            lines.append("📍 Place: not filled")

        if plan_info.exercise:
            lines.append(f"💪 Exercise: {plan_info.exercise.name}")
        else:
            lines.append("💪 Exercise: not filled")

        if plan_info.exercise_type is not None:
            lines.append(f"🏃 Exercise Type: {plan_info.exercise_type}")
        else:
            lines.append("🏃 Exercise Type: not filled")

        if plan_info.description:
            lines.append("")
            lines.append("🎯 *Personalized Recommendations:*")
            lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            lines.append(f"📋 {plan_info.description}")

        return "\n".join(lines)
