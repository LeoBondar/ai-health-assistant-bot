from aiogram.fsm.state import State, StatesGroup


class MainMenuStates(StatesGroup):
    main_menu = State("main_menu")


class CreateChatStates(StatesGroup):
    waiting_for_name = State("waiting_for_name")


class ActiveChatStates(StatesGroup):
    in_chat = State("in_chat")
