import contextlib

import orjson
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.strategy import FSMStrategy
from redis.asyncio.client import Redis

from bot import utils
from bot.common.bot_commands import set_commands
from bot.dependencies.di_container import DIContainer
from bot.handlers import setup_routers
from bot.persistent import init_mappers
from bot.settings import settings

bot = Bot(
    token=settings.bot.token,
    default=DefaultBotProperties(
        parse_mode=settings.bot.parse_mode,
    ),
)

dp = Dispatcher(
    fsm_strategy=FSMStrategy.USER_IN_CHAT,
    storage=(
        RedisStorage(redis=Redis(host=settings.redis.host, port=settings.redis.expose_port))
        if settings.redis.use
        else MemoryStorage()
    ),
)

def setup_logging(dp: Dispatcher) -> None:
    dp["infrastructure"] = utils.logging.setup_logger().bind(type="infrastructure")
    dp["db_logger"] = utils.logging.setup_logger().bind(type="db")
    dp["cache_logger"] = utils.logging.setup_logger().bind(type="cache")
    dp["business_logger"] = utils.logging.setup_logger().bind(type="business")

def setup_middlewares(dp: Dispatcher) -> None:
    pass

async def setup_bot() -> tuple[Dispatcher, Bot]:
    container = DIContainer()
    container.init_resources()
    await container.client_factory.provides.init_all()

    aiogram_session_logger = utils.logging.setup_logger().bind(type="aiogram_session")
    session = utils.smart_session.SmartAiogramAiohttpSession(
        json_loads=orjson.loads,
        logger=aiogram_session_logger,
    )
    bot.session = session

    await set_commands(bot)

    setup_middlewares(dp)
    setup_logging(dp)
    setup_routers(dp)
    init_mappers()

    await bot.delete_webhook(drop_pending_updates=settings.bot.drop_pending_updates)
    return dp, bot

async def main() -> None:
    dp, bot = await setup_bot()
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        await dp.start_polling(bot)
