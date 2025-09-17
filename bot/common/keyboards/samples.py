from aiogram.types import InlineKeyboardMarkup

from bot.adapters.ai_health.schemas import ChatInfo
from bot.common.keyboards.inline.callbacks import Action, ChatAction
from bot.common.keyboards.inline.consts import InlineConstructor
from bot.common.keyboards.keys import BACK_TO_MENU, CANCEL, CREATE_CHAT


def create_main_menu_keyboard(user_chats: list[ChatInfo]) -> InlineKeyboardMarkup:
    actions = []

    for chat in user_chats:
        actions.append({"text": f"💬 {chat.name}", "callback_data": ChatAction(action="open", chat_id=chat.id)})

    actions.append({"text": CREATE_CHAT, "callback_data": Action(action=CREATE_CHAT)})

    num_chats = len(user_chats)
    if num_chats == 0:
        schema = [1]
    else:
        chat_rows = []
        for i in range(0, num_chats, 2):
            remaining_chats = num_chats - i
            chat_rows.append(min(2, remaining_chats))
        schema = chat_rows + [1]
    return InlineConstructor._create_kb(
        actions=actions,
        schema=schema,
    )  # type: ignore[arg-type]


def create_cancel_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру с кнопкой отмены."""
    return InlineConstructor._create_kb(
        actions=[{"text": CANCEL, "callback_data": Action(action=CANCEL)}],
        schema=[1],
    )  # type: ignore[arg-type]


def create_chat_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру для режима чата с кнопкой возврата в главное меню."""
    return InlineConstructor._create_kb(
        actions=[{"text": BACK_TO_MENU, "callback_data": Action(action=BACK_TO_MENU)}],
        schema=[1],
    )  # type: ignore[arg-type]
