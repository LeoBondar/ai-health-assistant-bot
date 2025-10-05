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

        return PlanFillingStates.plan_completed.state

    @staticmethod
    def is_plan_complete(plan_info: AIAGetPlanInfoResponse) -> bool:

        return (
            plan_info.risk_factor is not None
            and plan_info.disease is not None
            and plan_info.user_goal is not None
            and plan_info.place is not None
            and plan_info.exercise is not None
        )

    @staticmethod
    def format_plan_info(plan_info: AIAGetPlanInfoResponse) -> str:

        lines = []

        if plan_info.risk_factor:
            lines.append(f"🔍 Фактор риска: {plan_info.risk_factor.factor}")
        else:
            lines.append("🔍 Фактор риска: не заполнено")

        if plan_info.disease:
            lines.append(f"🏥 Заболевание: {plan_info.disease.name}")
        else:
            lines.append("🏥 Заболевание: не заполнено")

        if plan_info.user_goal:
            lines.append(f"🎯 Цель: {plan_info.user_goal.name}")
        else:
            lines.append("🎯 Цель: не заполнено")

        if plan_info.place:
            lines.append(f"📍 Место: {plan_info.place.name}")
        else:
            lines.append("📍 Место: не заполнено")

        if plan_info.exercise:
            lines.append(f"💪 Упражнение: {plan_info.exercise.name} ({plan_info.exercise.type})")
        else:
            lines.append("💪 Упражнение: не заполнено")

        if plan_info.description:
            lines.append("")
            lines.append("🎯 *Персональные рекомендации:*")
            lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            lines.append(f"📋 {plan_info.description}")

        return "\n".join(lines)
