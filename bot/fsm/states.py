from aiogram.fsm.state import State, StatesGroup


class MainMenuStates(StatesGroup):
    main_menu = State("main_menu")


class CreateChatStates(StatesGroup):
    waiting_for_name = State("waiting_for_name")


class ActiveChatStates(StatesGroup):
    in_chat = State("in_chat")


class PlanFillingStates(StatesGroup):
    choosing_factor = State("choosing_factor")
    entering_disease = State("entering_disease")
    choosing_goal = State("choosing_goal")
    choosing_place = State("choosing_place")
    choosing_exercise = State("choosing_exercise")
    plan_completed = State("plan_completed")


class UpdatePlanStates(StatesGroup):
    waiting_for_preferences = State("waiting_for_preferences")
