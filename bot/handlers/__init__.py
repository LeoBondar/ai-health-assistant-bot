from aiogram import Dispatcher, Router
from loguru import logger

from bot.handlers.start.start import router as start_router

all_routers: list[Router] = [start_router]

def setup_routers(dp: Dispatcher) -> None:

    dp.include_routers(*all_routers)

__all__ = [
    "setup_routers",
]
