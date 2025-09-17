from dependency_injector import containers, providers

from bot.adapters.ai_health.adapter import AIHealthAdapter
from bot.infrastructure.http_client.ai_health.client import AIHealthHTTPClient
from bot.infrastructure.http_client.enums import ClientsEnum
from bot.infrastructure.http_client.factory import HttpClientsFactory
from bot.settings import Settings
from bot.views.service.add_chat import AddChatView
from bot.views.service.get_chats import GetUserChatsView
from bot.views.service.send_message import AddChatMessageView


class DIContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["bot.handlers", __name__])
    settings: providers.Singleton[Settings] = providers.Singleton(Settings)

    # Clients
    client_factory: providers.Singleton[HttpClientsFactory] = providers.Singleton(HttpClientsFactory)
    ai_health_client: providers.Factory[AIHealthHTTPClient] = providers.Factory(
        client_factory.provided(), client_name=ClientsEnum.AI_HEALTH
    )

    # Adapters
    ai_health_adapter: providers.Factory[AIHealthAdapter] = providers.Factory(AIHealthAdapter, client=ai_health_client)

    # Views
    get_user_chats_view: providers.Factory[GetUserChatsView] = providers.Factory(
        GetUserChatsView, adapter=ai_health_adapter
    )
    add_chat_view: providers.Factory[AddChatView] = providers.Factory(AddChatView, adapter=ai_health_adapter)
    add_chat_message_view: providers.Factory[AddChatMessageView] = providers.Factory(
        AddChatMessageView, adapter=ai_health_adapter
    )
