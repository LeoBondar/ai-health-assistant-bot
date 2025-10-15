from uuid import UUID

from bot.infrastructure.http_client.models import ApiCamelModel


class AIAAddChatCommand(ApiCamelModel):
    name: str | None = None
    user_id: str
    use_context: bool = True


class AIADeleteChatCommand(ApiCamelModel):
    chat_id: UUID


class AIAGetUserChatCommand(ApiCamelModel):
    limit: int = 10
    offset: int = 0
    user_id: str


class AIAAddMessageCommand(ApiCamelModel):
    chat_id: UUID
    user_id: str
    text: str


class AIAAddPlanFactorCommand(ApiCamelModel):
    plan_id: UUID
    factor_id: UUID


class AIAAddPlanPlaceCommand(ApiCamelModel):
    plan_id: UUID
    place_id: UUID


class AIAAddPlanExerciseCommand(ApiCamelModel):
    plan_id: UUID
    exercise_id: UUID


class AIAAddPlanGoalCommand(ApiCamelModel):
    plan_id: UUID
    goal_id: UUID


class AIAAddPlanDiseaseCommand(ApiCamelModel):
    plan_id: UUID
    name: str


class AIAGeneratePlanCommand(ApiCamelModel):
    plan_id: UUID


class AIAUpdatePlanCommand(ApiCamelModel):
    plan_id: UUID
    comment: str


class AIAGetPlanInfoCommand(ApiCamelModel):
    plan_id: UUID


class AIAGetRiskFactorsCommand(ApiCamelModel):
    limit: int = 10
    offset: int = 0


class AIAGetPlacesCommand(ApiCamelModel):
    limit: int = 10
    offset: int = 0


class AIAGetExercisesCommand(ApiCamelModel):
    limit: int = 10
    offset: int = 0


class AIAGetUserGoalsCommand(ApiCamelModel):
    limit: int = 10
    offset: int = 0


class AIAAddChatResponse(ApiCamelModel):
    id: UUID


class AIADeleteChatResponse(ApiCamelModel):
    pass


class ChatData(ApiCamelModel):
    id: UUID
    name: str
    plan_id: UUID
    use_context: bool


class AIAGetUserChatResponse(ApiCamelModel):
    chats: list[ChatData]


class AIAAddMessageResponse(ApiCamelModel):
    text: str


class RiskFactorData(ApiCamelModel):
    id: UUID
    factor: str


class AIAGetRiskFactorsResponse(ApiCamelModel):
    factors: list[RiskFactorData]


class PlaceData(ApiCamelModel):
    id: UUID
    name: str


class AIAGetPlacesResponse(ApiCamelModel):
    places: list[PlaceData]


class ExerciseData(ApiCamelModel):
    id: UUID
    name: str
    type: str


class AIAGetExercisesResponse(ApiCamelModel):
    exercises: list[ExerciseData]


class UserGoalData(ApiCamelModel):
    id: UUID
    name: str


class AIAGetUserGoalsResponse(ApiCamelModel):
    goals: list[UserGoalData]


class DiseaseData(ApiCamelModel):
    id: UUID
    name: str


class AIAGetPlanInfoResponse(ApiCamelModel):
    id: UUID
    description: str | None = None
    risk_factor: RiskFactorData | None = None
    disease: DiseaseData | None = None
    user_goal: UserGoalData | None = None
    place: PlaceData | None = None
    exercise: ExerciseData | None = None


class AIAAddPlanFactorResponse(ApiCamelModel):
    pass


class AIAAddPlanPlaceResponse(ApiCamelModel):
    pass


class AIAAddPlanExerciseResponse(ApiCamelModel):
    pass


class AIAAddPlanGoalResponse(ApiCamelModel):
    pass


class AIAAddPlanDiseaseResponse(ApiCamelModel):
    pass


class AIAGeneratePlanResponse(ApiCamelModel):
    description: str


class AIAUpdatePlanResponse(ApiCamelModel):
    description: str
