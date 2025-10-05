import json
from typing import Protocol

from bot.adapters.ai_health.schemas import (
    AIAAddChatCommand,
    AIAAddChatResponse,
    AIAAddMessageCommand,
    AIAAddMessageResponse,
    AIAAddPlanDiseaseCommand,
    AIAAddPlanDiseaseResponse,
    AIAAddPlanExerciseCommand,
    AIAAddPlanExerciseResponse,
    AIAAddPlanFactorCommand,
    AIAAddPlanFactorResponse,
    AIAAddPlanGoalCommand,
    AIAAddPlanGoalResponse,
    AIAAddPlanPlaceCommand,
    AIAAddPlanPlaceResponse,
    AIAGeneratePlanCommand,
    AIAGeneratePlanResponse,
    AIAGetExercisesCommand,
    AIAGetExercisesResponse,
    AIAGetPlacesCommand,
    AIAGetPlacesResponse,
    AIAGetPlanInfoCommand,
    AIAGetPlanInfoResponse,
    AIAGetRiskFactorsCommand,
    AIAGetRiskFactorsResponse,
    AIAGetUserChatCommand,
    AIAGetUserChatResponse,
    AIAGetUserGoalsCommand,
    AIAGetUserGoalsResponse,
)
from bot.infrastructure.http_client.ai_health.client import AIHealthHTTPClient
from bot.infrastructure.http_client.ai_health.schemas import (
    AIHCAddChatCommand,
    AIHCAddMessageCommand,
    AIHCAddPlanDiseaseCommand,
    AIHCAddPlanExerciseCommand,
    AIHCAddPlanFactorCommand,
    AIHCAddPlanGoalCommand,
    AIHCAddPlanPlaceCommand,
    AIHCGeneratePlanCommand,
    AIHCGetExercisesCommand,
    AIHCGetPlacesCommand,
    AIHCGetPlanInfoCommand,
    AIHCGetRiskFactorsCommand,
    AIHCGetUserChatCommand,
    AIHCGetUserGoalsCommand,
)


class IAIHealthAdapter(Protocol):

    async def add_chat(self, command: AIAAddChatCommand) -> AIAAddChatResponse:
        pass

    async def get_chats(self, command: AIAGetUserChatCommand) -> AIAGetUserChatResponse:
        pass

    async def add_chat_message(self, command: AIAAddMessageCommand) -> AIAAddMessageResponse:
        pass

    async def get_risk_factors(self, command: AIAGetRiskFactorsCommand) -> AIAGetRiskFactorsResponse:
        pass

    async def get_places(self, command: AIAGetPlacesCommand) -> AIAGetPlacesResponse:
        pass

    async def get_exercises(self, command: AIAGetExercisesCommand) -> AIAGetExercisesResponse:
        pass

    async def get_user_goals(self, command: AIAGetUserGoalsCommand) -> AIAGetUserGoalsResponse:
        pass

    async def add_plan_factor(self, command: AIAAddPlanFactorCommand) -> AIAAddPlanFactorResponse:
        pass

    async def add_plan_place(self, command: AIAAddPlanPlaceCommand) -> AIAAddPlanPlaceResponse:
        pass

    async def add_plan_exercise(self, command: AIAAddPlanExerciseCommand) -> AIAAddPlanExerciseResponse:
        pass

    async def add_plan_goal(self, command: AIAAddPlanGoalCommand) -> AIAAddPlanGoalResponse:
        pass

    async def add_plan_disease(self, command: AIAAddPlanDiseaseCommand) -> AIAAddPlanDiseaseResponse:
        pass

    async def get_plan_info(self, command: AIAGetPlanInfoCommand) -> AIAGetPlanInfoResponse:
        pass

    async def generate_plan(self, command: AIAGeneratePlanCommand) -> AIAGeneratePlanResponse:
        pass


class AIHealthAdapter(IAIHealthAdapter):
    def __init__(self, client: AIHealthHTTPClient):
        self._client = client

    async def get_chats(self, command: AIAGetUserChatCommand) -> AIAGetUserChatResponse:
        response = await self._client.get_user_chat(
            command=AIHCGetUserChatCommand(limit=command.limit, offset=command.offset, user_id=command.user_id)
        )
        body = json.loads(await response.text())
        return AIAGetUserChatResponse(**body["result"])

    async def add_chat_message(self, command: AIAAddMessageCommand) -> AIAAddMessageResponse:
        response = await self._client.add_chat_message(
            command=AIHCAddMessageCommand(chat_id=str(command.chat_id), user_id=command.user_id, text=command.text)
        )
        body = json.loads(await response.text())
        return AIAAddMessageResponse(**body["result"])

    async def add_chat(self, command: AIAAddChatCommand) -> AIAAddChatResponse:
        response = await self._client.add_user_chat(
            command=AIHCAddChatCommand(name=command.name, user_id=command.user_id, use_context=command.use_context)
        )
        body = json.loads(await response.text())
        return AIAAddChatResponse(**body["result"])

    async def get_risk_factors(self, command: AIAGetRiskFactorsCommand) -> AIAGetRiskFactorsResponse:
        response = await self._client.get_risk_factors(
            command=AIHCGetRiskFactorsCommand(limit=command.limit, offset=command.offset)
        )
        body = json.loads(await response.text())
        return AIAGetRiskFactorsResponse(**body["result"])

    async def get_places(self, command: AIAGetPlacesCommand) -> AIAGetPlacesResponse:
        response = await self._client.get_places(
            command=AIHCGetPlacesCommand(limit=command.limit, offset=command.offset)
        )
        body = json.loads(await response.text())
        return AIAGetPlacesResponse(**body["result"])

    async def get_exercises(self, command: AIAGetExercisesCommand) -> AIAGetExercisesResponse:
        response = await self._client.get_exercises(
            command=AIHCGetExercisesCommand(limit=command.limit, offset=command.offset)
        )
        body = json.loads(await response.text())
        return AIAGetExercisesResponse(**body["result"])

    async def get_user_goals(self, command: AIAGetUserGoalsCommand) -> AIAGetUserGoalsResponse:
        response = await self._client.get_user_goals(
            command=AIHCGetUserGoalsCommand(limit=command.limit, offset=command.offset)
        )
        body = json.loads(await response.text())
        return AIAGetUserGoalsResponse(**body["result"])

    async def add_plan_factor(self, command: AIAAddPlanFactorCommand) -> AIAAddPlanFactorResponse:
        response = await self._client.add_plan_factor(
            command=AIHCAddPlanFactorCommand(plan_id=str(command.plan_id), factor_id=str(command.factor_id))
        )
        body = json.loads(await response.text())
        return AIAAddPlanFactorResponse(**body["result"])

    async def add_plan_place(self, command: AIAAddPlanPlaceCommand) -> AIAAddPlanPlaceResponse:
        response = await self._client.add_plan_place(
            command=AIHCAddPlanPlaceCommand(plan_id=str(command.plan_id), place_id=str(command.place_id))
        )
        body = json.loads(await response.text())
        return AIAAddPlanPlaceResponse(**body["result"])

    async def add_plan_exercise(self, command: AIAAddPlanExerciseCommand) -> AIAAddPlanExerciseResponse:
        response = await self._client.add_plan_exercise(
            command=AIHCAddPlanExerciseCommand(plan_id=str(command.plan_id), exercise_id=str(command.exercise_id))
        )
        body = json.loads(await response.text())
        return AIAAddPlanExerciseResponse(**body["result"])

    async def add_plan_goal(self, command: AIAAddPlanGoalCommand) -> AIAAddPlanGoalResponse:
        response = await self._client.add_plan_goal(
            command=AIHCAddPlanGoalCommand(plan_id=str(command.plan_id), goal_id=str(command.goal_id))
        )
        body = json.loads(await response.text())
        return AIAAddPlanGoalResponse(**body["result"])

    async def add_plan_disease(self, command: AIAAddPlanDiseaseCommand) -> AIAAddPlanDiseaseResponse:
        response = await self._client.add_plan_disease(
            command=AIHCAddPlanDiseaseCommand(plan_id=str(command.plan_id), name=command.name)
        )
        body = json.loads(await response.text())
        return AIAAddPlanDiseaseResponse(**body["result"])

    async def get_plan_info(self, command: AIAGetPlanInfoCommand) -> AIAGetPlanInfoResponse:
        response = await self._client.get_plan_info(command=AIHCGetPlanInfoCommand(plan_id=str(command.plan_id)))
        body = json.loads(await response.text())
        return AIAGetPlanInfoResponse(**body["result"])

    async def generate_plan(self, command: AIAGeneratePlanCommand) -> AIAGeneratePlanResponse:
        response = await self._client.generate_plan(command=AIHCGeneratePlanCommand(plan_id=str(command.plan_id)))
        body = json.loads(await response.text())
        return AIAGeneratePlanResponse(**body["result"])
