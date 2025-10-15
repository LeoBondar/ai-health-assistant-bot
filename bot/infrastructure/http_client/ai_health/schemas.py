from uuid import UUID

from bot.infrastructure.http_client.models import ApiCamelModel


class AIHCAddChatCommand(ApiCamelModel):
    name: str | None = None
    user_id: str
    use_context: bool = True


class AIHCDeleteChatCommand(ApiCamelModel):
    chat_id: str


class AIHCGetUserChatCommand(ApiCamelModel):
    limit: int = 10
    offset: int = 0
    user_id: str


class AIHCAddMessageCommand(ApiCamelModel):
    chat_id: str
    user_id: str
    text: str


class AIHCAddPlanFactorCommand(ApiCamelModel):
    plan_id: str
    factor_id: str


class AIHCAddPlanPlaceCommand(ApiCamelModel):
    plan_id: str
    place_id: str


class AIHCAddPlanExerciseCommand(ApiCamelModel):
    plan_id: str
    exercise_id: str


class AIHCAddPlanGoalCommand(ApiCamelModel):
    plan_id: str
    goal_id: str


class AIHCAddPlanDiseaseCommand(ApiCamelModel):
    plan_id: str
    name: str


class AIHCGetRiskFactorsCommand(ApiCamelModel):
    limit: int = 10
    offset: int = 0


class AIHCGetPlacesCommand(ApiCamelModel):
    limit: int = 10
    offset: int = 0


class AIHCGetExercisesCommand(ApiCamelModel):
    limit: int = 10
    offset: int = 0


class AIHCGetUserGoalsCommand(ApiCamelModel):
    limit: int = 10
    offset: int = 0


class AIHCGetPlanInfoCommand(ApiCamelModel):
    plan_id: str


class AIHCGeneratePlanCommand(ApiCamelModel):
    plan_id: str


class AIHCUpdatePlanCommand(ApiCamelModel):
    plan_id: str
    comment: str
