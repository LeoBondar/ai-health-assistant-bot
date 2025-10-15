from dependency_injector import containers, providers

from bot.adapters.ai_health.adapter import AIHealthAdapter
from bot.infrastructure.http_client.ai_health.client import AIHealthHTTPClient
from bot.infrastructure.http_client.enums import ClientsEnum
from bot.infrastructure.http_client.factory import HttpClientsFactory
from bot.settings import Settings
from bot.views.service.add_chat import AddChatView
from bot.views.service.add_plan_disease import AddPlanDiseaseView
from bot.views.service.add_plan_exercise import AddPlanExerciseView
from bot.views.service.add_plan_factor import AddPlanFactorView
from bot.views.service.add_plan_goal import AddPlanGoalView
from bot.views.service.add_plan_place import AddPlanPlaceView
from bot.views.service.delete_chat import DeleteChatView
from bot.views.service.generate_plan import GeneratePlanView
from bot.views.service.get_chats import GetUserChatsView
from bot.views.service.get_exercises import GetExercisesView
from bot.views.service.get_places import GetPlacesView
from bot.views.service.get_plan_info import GetPlanInfoView
from bot.views.service.get_risk_factors import GetRiskFactorsView
from bot.views.service.get_user_goals import GetUserGoalsView
from bot.views.service.send_message import AddChatMessageView
from bot.views.service.update_plan import UpdatePlanView


class DIContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["bot.handlers", __name__])
    settings: providers.Singleton[Settings] = providers.Singleton(Settings)

    client_factory: providers.Singleton[HttpClientsFactory] = providers.Singleton(HttpClientsFactory)
    ai_health_client: providers.Factory[AIHealthHTTPClient] = providers.Factory(
        client_factory.provided(), client_name=ClientsEnum.AI_HEALTH
    )

    ai_health_adapter: providers.Factory[AIHealthAdapter] = providers.Factory(AIHealthAdapter, client=ai_health_client)

    get_user_chats_view: providers.Factory[GetUserChatsView] = providers.Factory(
        GetUserChatsView, adapter=ai_health_adapter
    )
    add_chat_view: providers.Factory[AddChatView] = providers.Factory(AddChatView, adapter=ai_health_adapter)
    delete_chat_view: providers.Factory[DeleteChatView] = providers.Factory(DeleteChatView, adapter=ai_health_adapter)
    add_chat_message_view: providers.Factory[AddChatMessageView] = providers.Factory(
        AddChatMessageView, adapter=ai_health_adapter
    )

    get_plan_info_view: providers.Factory[GetPlanInfoView] = providers.Factory(
        GetPlanInfoView, adapter=ai_health_adapter
    )
    get_risk_factors_view: providers.Factory[GetRiskFactorsView] = providers.Factory(
        GetRiskFactorsView, adapter=ai_health_adapter
    )
    get_user_goals_view: providers.Factory[GetUserGoalsView] = providers.Factory(
        GetUserGoalsView, adapter=ai_health_adapter
    )
    get_places_view: providers.Factory[GetPlacesView] = providers.Factory(GetPlacesView, adapter=ai_health_adapter)
    get_exercises_view: providers.Factory[GetExercisesView] = providers.Factory(
        GetExercisesView, adapter=ai_health_adapter
    )
    add_plan_factor_view: providers.Factory[AddPlanFactorView] = providers.Factory(
        AddPlanFactorView, adapter=ai_health_adapter
    )
    add_plan_disease_view: providers.Factory[AddPlanDiseaseView] = providers.Factory(
        AddPlanDiseaseView, adapter=ai_health_adapter
    )
    add_plan_goal_view: providers.Factory[AddPlanGoalView] = providers.Factory(
        AddPlanGoalView, adapter=ai_health_adapter
    )
    add_plan_place_view: providers.Factory[AddPlanPlaceView] = providers.Factory(
        AddPlanPlaceView, adapter=ai_health_adapter
    )
    add_plan_exercise_view: providers.Factory[AddPlanExerciseView] = providers.Factory(
        AddPlanExerciseView, adapter=ai_health_adapter
    )
    generate_plan_view: providers.Factory[GeneratePlanView] = providers.Factory(
        GeneratePlanView, adapter=ai_health_adapter
    )
    update_plan_view: providers.Factory[UpdatePlanView] = providers.Factory(UpdatePlanView, adapter=ai_health_adapter)
