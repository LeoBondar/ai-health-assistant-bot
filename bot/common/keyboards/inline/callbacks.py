from typing import Optional
from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class Action(CallbackData, prefix="act"):
    action: str


class ChatAction(CallbackData, prefix="chat"):
    action: str  # "open", "delete", etc.
    chat_id: UUID
