from aiogram.fsm.context import FSMContext

from bot.fsm.states import MainMenuStates

class FSMMainMenuManager:
    @staticmethod
    async def set_main_menu_state(state: FSMContext) -> None:
        await state.set_state(MainMenuStates.main_menu)

    @staticmethod
    async def reset_main_menu_state(state: FSMContext) -> None:
        await state.set_state(None)
