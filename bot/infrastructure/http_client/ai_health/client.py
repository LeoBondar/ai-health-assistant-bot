from typing import Any
from urllib.parse import urljoin

from aiohttp import ClientResponse, ClientTimeout, TCPConnector

from bot.infrastructure.http_client.ai_health.schemas import (
    AIHCAddChatCommand,
    AIHCAddMessageCommand,
    AIHCAddPlanDiseaseCommand,
    AIHCAddPlanExerciseCommand,
    AIHCAddPlanFactorCommand,
    AIHCAddPlanGoalCommand,
    AIHCAddPlanPlaceCommand,
    AIHCDeleteChatCommand,
    AIHCGeneratePlanCommand,
    AIHCGetExercisesCommand,
    AIHCGetPlacesCommand,
    AIHCGetPlanInfoCommand,
    AIHCGetRiskFactorsCommand,
    AIHCGetUserChatCommand,
    AIHCGetUserGoalsCommand,
    AIHCSetPlanExerciseTypeCommand,
    AIHCUpdatePlanCommand,
)
from bot.infrastructure.http_client.base import BaseHTTPClient
from bot.infrastructure.http_client.enums import RequestMethodType
from bot.settings import settings

class AIHealthHTTPClient(BaseHTTPClient):

    async def add_user_chat(self, command: AIHCAddChatCommand) -> ClientResponse:
        return await self._make_request(
            uri="/api/v1/chats/",
            method=RequestMethodType.POST,
            body=command.model_dump(),
        )

    async def delete_chat(self, command: AIHCDeleteChatCommand) -> ClientResponse:
        return await self._make_request(
            uri=f"/api/v1/chats/{command.chat_id}",
            method=RequestMethodType.DELETE,
        )

    async def get_user_chat(self, command: AIHCGetUserChatCommand) -> ClientResponse:
        return await self._make_request(
            uri="/api/v1/chats/",
            method=RequestMethodType.GET,
            params={"limit": command.limit, "offset": command.offset, "userId": command.user_id},
        )

    async def add_chat_message(self, command: AIHCAddMessageCommand) -> ClientResponse:
        return await self._make_request(
            uri=f"/api/v1/chats/{command.chat_id}/message",
            method=RequestMethodType.POST,
            body={"text": command.text, "userId": command.user_id},
        )

    async def get_risk_factors(self, command: AIHCGetRiskFactorsCommand) -> ClientResponse:
        return await self._make_request(
            uri="/api/v1/chats/riskFactors",
            method=RequestMethodType.GET,
            params={"limit": command.limit, "offset": command.offset},
        )

    async def get_places(self, command: AIHCGetPlacesCommand) -> ClientResponse:
        return await self._make_request(
            uri="/api/v1/chats/places",
            method=RequestMethodType.GET,
            params={"limit": command.limit, "offset": command.offset},
        )

    async def get_exercises(self, command: AIHCGetExercisesCommand) -> ClientResponse:
        return await self._make_request(
            uri="/api/v1/chats/exercises",
            method=RequestMethodType.GET,
            params={"limit": command.limit, "offset": command.offset},
        )

    async def get_user_goals(self, command: AIHCGetUserGoalsCommand) -> ClientResponse:
        return await self._make_request(
            uri="/api/v1/chats/goals",
            method=RequestMethodType.GET,
            params={"limit": command.limit, "offset": command.offset},
        )

    async def add_plan_factor(self, command: AIHCAddPlanFactorCommand) -> ClientResponse:
        return await self._make_request(
            uri="/api/v1/chats/plans/riskFactor",
            method=RequestMethodType.POST,
            body=command.model_dump(),
        )

    async def add_plan_place(self, command: AIHCAddPlanPlaceCommand) -> ClientResponse:
        return await self._make_request(
            uri="/api/v1/chats/plans/place",
            method=RequestMethodType.POST,
            body=command.model_dump(),
        )

    async def add_plan_exercise(self, command: AIHCAddPlanExerciseCommand) -> ClientResponse:
        return await self._make_request(
            uri="/api/v1/chats/plans/exercise",
            method=RequestMethodType.POST,
            body=command.model_dump(),
        )

    async def add_plan_goal(self, command: AIHCAddPlanGoalCommand) -> ClientResponse:
        return await self._make_request(
            uri="/api/v1/chats/plans/goal",
            method=RequestMethodType.POST,
            body=command.model_dump(),
        )

    async def add_plan_disease(self, command: AIHCAddPlanDiseaseCommand) -> ClientResponse:
        return await self._make_request(
            uri="/api/v1/chats/plans/disease",
            method=RequestMethodType.POST,
            body=command.model_dump(),
        )

    async def get_plan_info(self, command: AIHCGetPlanInfoCommand) -> ClientResponse:
        return await self._make_request(
            uri=f"/api/v1/chats/plans/{command.plan_id}",
            method=RequestMethodType.GET,
        )

    async def generate_plan(self, command: AIHCGeneratePlanCommand) -> ClientResponse:
        return await self._make_request(
            uri=f"/api/v1/chats/plans/{command.plan_id}/generate",
            method=RequestMethodType.POST,
        )

    async def update_plan(self, command: AIHCUpdatePlanCommand) -> ClientResponse:
        return await self._make_request(
            uri="/api/v1/chats/plans",
            method=RequestMethodType.PUT,
            body=command.model_dump(),
        )
        
    async def set_plan_exercise_type(self, command: AIHCSetPlanExerciseTypeCommand) -> ClientResponse:
        return await self._make_request(
            uri=f"/api/v1/chats/plans/{command.plan_id}/exercise-type",
            method=RequestMethodType.POST,
            body=command.model_dump(),
        )

    async def _make_request(
        self,
        method: RequestMethodType,
        uri: str,
        body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> ClientResponse:
        return await self._request(
            method=method,
            json=body,
            params=params,
            str_or_url=urljoin(settings.ai.base_url, uri),
            ssl=settings.ai.validate_cert,
            timeout=ClientTimeout(total=settings.ai.total_timeout, connect=settings.ai.connect_timeout),
        )

    @staticmethod
    def get_session_config() -> dict[str, Any]:
        return {
            "connector": TCPConnector(limit=settings.ai.connection_limit),
        }
