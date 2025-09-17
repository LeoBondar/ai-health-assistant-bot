from uuid import UUID

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from dependency_injector.wiring import Provide, inject

from bot.common.keyboards.inline.callbacks import Action, ChatAction
from bot.common.keyboards.keys import BACK_TO_MENU, CANCEL, CREATE_CHAT
from bot.common.keyboards.samples import create_cancel_keyboard, create_chat_keyboard, create_main_menu_keyboard
from bot.common.messages import (
    AI_RESPONSE_MESSAGE,
    BACK_TO_MENU_MESSAGE,
    CHAT_CREATED_SUCCESS_MESSAGE,
    CHAT_OPENED_MESSAGE,
    ENTER_CHAT_NAME_MESSAGE,
    ERROR_CHAT_CREATION_MESSAGE,
    ERROR_CHAT_ID_NOT_FOUND,
    ERROR_EMPTY_CHAT_NAME_MESSAGE,
    ERROR_MESSAGE_SEND_FAILED,
    ERROR_TEXT_MESSAGE_ONLY,
    ERROR_TEXT_ONLY_MESSAGE,
    GREETINGS_MESSAGE,
    OPERATION_CANCELLED_MESSAGE,
    PROCESSING_MESSAGE,
)
from bot.dependencies.di_container import DIContainer
from bot.fsm.managers.main_menu import FSMMainMenuManager
from bot.fsm.states import ActiveChatStates, CreateChatStates
from bot.views.service.add_chat import AddChatView
from bot.views.service.get_chats import GetUserChatsView
from bot.views.service.send_message import AddChatMessageView

router = Router(name="start")


@router.message(Command("start", "help"))
@inject
async def handle_start(
    message: types.Message,
    state: FSMContext,
    view: GetUserChatsView = Provide[DIContainer.get_user_chats_view],
) -> None:
    await FSMMainMenuManager.reset_main_menu_state(state)
    user_chats_response = await view(message.from_user.id)  # type: ignore[union-attr]
    keyboard = create_main_menu_keyboard(user_chats_response.chats)

    await message.answer(GREETINGS_MESSAGE, reply_markup=keyboard, user_id=message.from_user.id)  # type: ignore[union-attr]


@router.callback_query(ChatAction.filter(F.action == "open"))
async def handle_open_chat(
    callback: types.CallbackQuery,
    callback_data: ChatAction,
    state: FSMContext,
) -> None:
    await state.update_data(active_chat_id=str(callback_data.chat_id))

    await state.set_state(ActiveChatStates.in_chat)

    if callback.message:
        await callback.message.edit_text(
            f"💬 Вы в чате!\n\n� Напишите сообщение, и я отправлю его в чат {callback_data.chat_id}",
            reply_markup=create_chat_keyboard(),
        )
    await callback.answer()


@router.callback_query(Action.filter(F.action == CREATE_CHAT))
async def handle_create_chat(
    callback: types.CallbackQuery,
    callback_data: Action,
    state: FSMContext,
) -> None:
    if callback.message:
        await callback.message.edit_text(ENTER_CHAT_NAME_MESSAGE, reply_markup=create_cancel_keyboard())

    await state.set_state(CreateChatStates.waiting_for_name)
    await callback.answer()


@router.message(CreateChatStates.waiting_for_name)
@inject
async def handle_chat_name_input(
    message: types.Message,
    state: FSMContext,
    get_chats_view: GetUserChatsView = Provide[DIContainer.get_user_chats_view],
    add_chat_view: AddChatView = Provide[DIContainer.add_chat_view],
) -> None:
    if not message.text:
        await message.answer(ERROR_TEXT_ONLY_MESSAGE)
        return

    chat_name = message.text.strip()
    if not chat_name:
        await message.answer(ERROR_EMPTY_CHAT_NAME_MESSAGE)
        return

    try:
        add_result = await add_chat_view(message.from_user.id, chat_name)  # type: ignore[union-attr]
        user_chats_response = await get_chats_view(message.from_user.id)  # type: ignore[union-attr]
        keyboard = create_main_menu_keyboard(user_chats_response.chats)

        await message.answer(
            f"{CHAT_CREATED_SUCCESS_MESSAGE.format(chat_name=chat_name)}\n\n{GREETINGS_MESSAGE}", reply_markup=keyboard
        )

        await FSMMainMenuManager.reset_main_menu_state(state)

    except Exception as e:
        await message.answer(ERROR_CHAT_CREATION_MESSAGE.format(error=str(e)))
        await FSMMainMenuManager.reset_main_menu_state(state)

        user_chats_response = await get_chats_view(message.from_user.id)  # type: ignore[union-attr]
        keyboard = create_main_menu_keyboard(user_chats_response.chats)
        await message.answer(GREETINGS_MESSAGE, reply_markup=keyboard)


@router.callback_query(Action.filter(F.action == CANCEL))
@inject
async def handle_cancel(
    callback: types.CallbackQuery,
    callback_data: Action,
    state: FSMContext,
    get_chats_view: GetUserChatsView = Provide[DIContainer.get_user_chats_view],
) -> None:
    await FSMMainMenuManager.reset_main_menu_state(state)

    user_chats_response = await get_chats_view(callback.from_user.id)
    keyboard = create_main_menu_keyboard(user_chats_response.chats)

    if callback.message:
        await callback.message.edit_text(GREETINGS_MESSAGE, reply_markup=keyboard)

    await callback.answer(OPERATION_CANCELLED_MESSAGE)


@router.message(ActiveChatStates.in_chat)
@inject
async def handle_chat_message(
    message: types.Message,
    state: FSMContext,
    add_message_view: AddChatMessageView = Provide[DIContainer.add_chat_message_view],
) -> None:
    if not message.text:
        await message.answer(ERROR_TEXT_MESSAGE_ONLY)
        return

    data = await state.get_data()
    active_chat_id = data.get("active_chat_id")

    if not active_chat_id:
        await message.answer(ERROR_CHAT_ID_NOT_FOUND)
        await FSMMainMenuManager.reset_main_menu_state(state)
        return

    processing_msg = await message.answer(PROCESSING_MESSAGE)

    try:
        response = await add_message_view(user_id=message.from_user.id, chat_id=UUID(active_chat_id), text=message.text)

        await processing_msg.delete()
        await message.answer(AI_RESPONSE_MESSAGE.format(response=response.text), reply_markup=create_chat_keyboard())

    except Exception as e:
        await processing_msg.delete()

        await message.answer(ERROR_MESSAGE_SEND_FAILED.format(error=str(e)), reply_markup=create_chat_keyboard())


@router.callback_query(Action.filter(F.action == BACK_TO_MENU))
@inject
async def handle_back_to_menu(
    callback: types.CallbackQuery,
    callback_data: Action,
    state: FSMContext,
    get_chats_view: GetUserChatsView = Provide[DIContainer.get_user_chats_view],
) -> None:
    await FSMMainMenuManager.reset_main_menu_state(state)

    user_chats_response = await get_chats_view(callback.from_user.id)
    keyboard = create_main_menu_keyboard(user_chats_response.chats)

    if callback.message:
        await callback.message.edit_text(GREETINGS_MESSAGE, reply_markup=keyboard)

    await callback.answer(BACK_TO_MENU_MESSAGE)
