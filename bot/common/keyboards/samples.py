from uuid import UUID

from aiogram.types import InlineKeyboardMarkup

from bot.adapters.ai_health.schemas import ChatData, ExerciseData, PlaceData, RiskFactorData, UserGoalData
from bot.common.keyboards.inline.callbacks import (
    Action,
    ChatAction,
    ExerciseAction,
    FactorAction,
    GoalAction,
    PlaceAction,
    PlanAction,
    shorten_uuid,
)
from bot.common.keyboards.inline.consts import InlineConstructor
from bot.common.keyboards.keys import (
    BACK_TO_MENU,
    CANCEL,
    CREATE_CHAT,
    DELETE_CHAT,
    EDIT_DISEASE,
    EDIT_EXERCISE,
    EDIT_GOAL,
    EDIT_PLACE,
    EDIT_RISK_FACTOR,
    FILL_PLAN,
    GET_RECOMMENDATIONS,
    SKIP_STEP,
    UPDATE_RECOMMENDATIONS,
)

def create_main_menu_keyboard(user_chats: list[ChatData]) -> InlineKeyboardMarkup:
    actions = []

    for chat in user_chats:
        actions.append(
            {"text": f"💬 {chat.name}", "callback_data": ChatAction(action="open", chat_id=shorten_uuid(chat.id))}
        )

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
    )

def create_cancel_keyboard() -> InlineKeyboardMarkup:
    return InlineConstructor._create_kb(
        actions=[{"text": CANCEL, "callback_data": Action(action=CANCEL)}],
        schema=[1],
    )

def create_chat_keyboard() -> InlineKeyboardMarkup:
    return InlineConstructor._create_kb(
        actions=[{"text": BACK_TO_MENU, "callback_data": Action(action=BACK_TO_MENU)}],
        schema=[1],
    )

def create_plan_keyboard(
    plan_id: UUID, chat_id: UUID, is_complete: bool, has_description: bool
) -> InlineKeyboardMarkup:
    actions = []

    if is_complete:
        if has_description:
            actions.append(
                {
                    "text": UPDATE_RECOMMENDATIONS,
                    "callback_data": PlanAction(action="update_recommendations", plan_id=shorten_uuid(plan_id)),
                }
            )
        else:
            actions.append(
                {
                    "text": GET_RECOMMENDATIONS,
                    "callback_data": PlanAction(action="generate_recommendations", plan_id=shorten_uuid(plan_id)),
                }
            )

        actions.extend(
            [
                {
                    "text": EDIT_RISK_FACTOR,
                    "callback_data": PlanAction(action="edit_risk_factor", plan_id=shorten_uuid(plan_id)),
                },
                {
                    "text": EDIT_DISEASE,
                    "callback_data": PlanAction(action="edit_disease", plan_id=shorten_uuid(plan_id)),
                },
                {
                    "text": EDIT_GOAL,
                    "callback_data": PlanAction(action="edit_goal", plan_id=shorten_uuid(plan_id)),
                },
                {
                    "text": EDIT_PLACE,
                    "callback_data": PlanAction(action="edit_place", plan_id=shorten_uuid(plan_id)),
                },
                {
                    "text": EDIT_EXERCISE,
                    "callback_data": PlanAction(action="edit_exercise", plan_id=shorten_uuid(plan_id)),
                },
            ]
        )
    else:
        actions.append({"text": FILL_PLAN, "callback_data": PlanAction(action="fill", plan_id=shorten_uuid(plan_id))})

    actions.append({"text": DELETE_CHAT, "callback_data": ChatAction(action="delete", chat_id=shorten_uuid(chat_id))})

    actions.append({"text": BACK_TO_MENU, "callback_data": Action(action=BACK_TO_MENU)})

    if is_complete:

        schema = [1, 2, 2, 1, 1, 1]
    else:

        schema = [1, 1, 1]

    return InlineConstructor._create_kb(
        actions=actions,
        schema=schema,
    )

def create_factors_keyboard(factors: list[RiskFactorData], plan_id: UUID) -> InlineKeyboardMarkup:
    actions = []

    for factor in factors:
        actions.append(
            {
                "text": factor.factor,
                "callback_data": FactorAction(factor_id=shorten_uuid(factor.id), plan_id=shorten_uuid(plan_id)),
            }
        )

    actions.append({"text": BACK_TO_MENU, "callback_data": Action(action=BACK_TO_MENU)})

    factor_rows = [1] * len(factors)
    schema = factor_rows + [1]

    return InlineConstructor._create_kb(
        actions=actions,
        schema=schema,
    )

def create_goals_keyboard(goals: list[UserGoalData], plan_id: UUID) -> InlineKeyboardMarkup:
    actions = []

    for goal in goals:
        actions.append(
            {
                "text": goal.name,
                "callback_data": GoalAction(goal_id=shorten_uuid(goal.id), plan_id=shorten_uuid(plan_id)),
            }
        )

    actions.append({"text": BACK_TO_MENU, "callback_data": Action(action=BACK_TO_MENU)})

    goal_rows = [1] * len(goals)
    schema = goal_rows + [1]

    return InlineConstructor._create_kb(
        actions=actions,
        schema=schema,
    )

def create_places_keyboard(places: list[PlaceData], plan_id: UUID) -> InlineKeyboardMarkup:
    actions = []

    for place in places:
        actions.append(
            {
                "text": place.name,
                "callback_data": PlaceAction(place_id=shorten_uuid(place.id), plan_id=shorten_uuid(plan_id)),
            }
        )

    actions.append({"text": BACK_TO_MENU, "callback_data": Action(action=BACK_TO_MENU)})

    place_rows = [1] * len(places)
    schema = place_rows + [1]

    return InlineConstructor._create_kb(
        actions=actions,
        schema=schema,
    )

def create_exercises_keyboard(exercises: list[ExerciseData], plan_id: UUID) -> InlineKeyboardMarkup:
    actions = []

    for exercise in exercises:
        actions.append(
            {
                "text": f"{exercise.name}",
                "callback_data": ExerciseAction(exercise_id=shorten_uuid(exercise.id), plan_id=shorten_uuid(plan_id)),
            }
        )

    actions.append({"text": BACK_TO_MENU, "callback_data": Action(action=BACK_TO_MENU)})

    exercise_rows = [1] * len(exercises)
    schema = exercise_rows + [1]

    return InlineConstructor._create_kb(
        actions=actions,
        schema=schema,
    )

def create_disease_input_keyboard() -> InlineKeyboardMarkup:
    return InlineConstructor._create_kb(
        actions=[
            {"text": SKIP_STEP, "callback_data": Action(action=SKIP_STEP)},
            {"text": BACK_TO_MENU, "callback_data": Action(action=BACK_TO_MENU)},
        ],
        schema=[1, 1],
    )

def create_preferences_input_keyboard() -> InlineKeyboardMarkup:
    return InlineConstructor._create_kb(
        actions=[
            {"text": BACK_TO_MENU, "callback_data": Action(action=BACK_TO_MENU)},
        ],
        schema=[1],
    )
