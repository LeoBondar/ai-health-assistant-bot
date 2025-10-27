from uuid import UUID

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from dependency_injector.wiring import Provide, inject

from bot.common.keyboards.inline.callbacks import (
    Action,
    ChatAction,
    ExerciseAction,
    FactorAction,
    GoalAction,
    PlaceAction,
    PlanAction,
    get_full_uuid,
    register_uuid_mapping,
)
from bot.common.keyboards.keys import (
    BACK_TO_MENU,
    CANCEL,
    CREATE_CHAT,
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
from bot.common.keyboards.samples import (
    create_cancel_keyboard,
    create_chat_keyboard,
    create_disease_input_keyboard,
    create_exercises_keyboard,
    create_factors_keyboard,
    create_goals_keyboard,
    create_main_menu_keyboard,
    create_places_keyboard,
    create_plan_keyboard,
    create_preferences_input_keyboard,
)
from bot.common.messages import (
    AI_RESPONSE_MESSAGE,
    BACK_TO_MENU_MESSAGE,
    CHAT_CREATED_SUCCESS_MESSAGE,
    CHOOSE_EXERCISE_MESSAGE,
    CHOOSE_GOAL_MESSAGE,
    CHOOSE_PLACE_MESSAGE,
    CHOOSE_RISK_FACTOR_MESSAGE,
    DISEASE_ADDED_MESSAGE,
    ENTER_CHAT_NAME_MESSAGE,
    ENTER_DISEASE_MESSAGE,
    ENTER_PREFERENCES_MESSAGE,
    ERROR_CHAT_CREATION_MESSAGE,
    ERROR_CHAT_ID_NOT_FOUND,
    ERROR_EMPTY_CHAT_NAME_MESSAGE,
    ERROR_EMPTY_DISEASE_NAME,
    ERROR_EMPTY_PREFERENCES_MESSAGE,
    ERROR_MESSAGE_SEND_FAILED,
    ERROR_TEXT_MESSAGE_ONLY,
    ERROR_TEXT_ONLY_MESSAGE,
    EXERCISE_ADDED_MESSAGE,
    FACTOR_ADDED_MESSAGE,
    GENERATING_RECOMMENDATIONS_MESSAGE,
    GOAL_ADDED_MESSAGE,
    GREETINGS_MESSAGE,
    OPERATION_CANCELLED_MESSAGE,
    PLACE_ADDED_MESSAGE,
    PLAN_EMPTY_MESSAGE,
    PLAN_INFO_MESSAGE,
    PLAN_READY_MESSAGE,
    PLAN_UPDATED_SUCCESS_MESSAGE,
    PROCESSING_MESSAGE,
    RECOMMENDATIONS_GENERATED_MESSAGE,
    RECOMMENDATIONS_UPDATED_MESSAGE,
    STEP_SKIPPED_MESSAGE,
    UPDATING_PLAN_MESSAGE,
)
from bot.dependencies.di_container import DIContainer
from bot.fsm.managers.main_menu import FSMMainMenuManager
from bot.fsm.states import ActiveChatStates, CreateChatStates, PlanFillingStates, UpdatePlanStates
from bot.utils.plan_helper import PlanFillingHelper
from bot.views.service.add_chat import AddChatView
from bot.views.service.add_plan_disease import AddPlanDiseaseView
from bot.views.service.add_plan_exercise import AddPlanExerciseView
from bot.views.service.add_plan_factor import AddPlanFactorView
from bot.views.service.add_plan_goal import AddPlanGoalView
from bot.views.service.add_plan_place import AddPlanPlaceView
from bot.views.service.delete_chat import DeleteChatView
from bot.views.service.generate_plan import GeneratePlanView
from bot.views.service.get_chats import GetUserChatsView
from bot.views.service.get_exercises import GetExercisesView
from bot.views.service.get_places import GetPlacesView
from bot.views.service.get_plan_info import GetPlanInfoView
from bot.views.service.get_risk_factors import GetRiskFactorsView
from bot.views.service.get_user_goals import GetUserGoalsView
from bot.views.service.send_message import AddChatMessageView
from bot.views.service.update_plan import UpdatePlanView

router = Router(name="start")

async def ensure_uuid_mapping_exists(user_id: int, get_chats_view: GetUserChatsView) -> None:
    user_chats_response = await get_chats_view(user_id)
    for chat in user_chats_response.chats:
        register_uuid_mapping(chat.id)
        register_uuid_mapping(chat.plan_id)

async def safe_get_full_uuid(short_uuid: str, user_id: int, get_chats_view: GetUserChatsView) -> UUID:
    try:
        return get_full_uuid(short_uuid)
    except ValueError:
        await ensure_uuid_mapping_exists(user_id, get_chats_view)
        return get_full_uuid(short_uuid)

async def get_chat_id_by_plan_id(plan_id: UUID, user_id: int, get_chats_view: GetUserChatsView) -> UUID:
    user_chats_response = await get_chats_view(user_id)
    for chat in user_chats_response.chats:
        if chat.plan_id == plan_id:
            return chat.id
    raise ValueError(f"Chat not found for plan_id: {plan_id}")

async def safe_get_factor_uuids(
    plan_short_uuid: str,
    factor_short_uuid: str,
    user_id: int,
    get_chats_view: GetUserChatsView,
    get_risk_factors_view: GetRiskFactorsView,
) -> tuple[UUID, UUID]:
    try:
        plan_id = get_full_uuid(plan_short_uuid)
        factor_id = get_full_uuid(factor_short_uuid)
        return plan_id, factor_id
    except ValueError:
        await ensure_uuid_mapping_exists(user_id, get_chats_view)
        factors_response = await get_risk_factors_view()
        for factor in factors_response.factors:
            register_uuid_mapping(factor.id)
        plan_id = get_full_uuid(plan_short_uuid)
        factor_id = get_full_uuid(factor_short_uuid)
        return plan_id, factor_id

async def safe_get_goal_uuids(
    plan_short_uuid: str,
    goal_short_uuid: str,
    user_id: int,
    get_chats_view: GetUserChatsView,
    get_user_goals_view: GetUserGoalsView,
) -> tuple[UUID, UUID]:
    try:
        plan_id = get_full_uuid(plan_short_uuid)
        goal_id = get_full_uuid(goal_short_uuid)
        return plan_id, goal_id
    except ValueError:
        await ensure_uuid_mapping_exists(user_id, get_chats_view)
        goals_response = await get_user_goals_view()
        for goal in goals_response.goals:
            register_uuid_mapping(goal.id)
        plan_id = get_full_uuid(plan_short_uuid)
        goal_id = get_full_uuid(goal_short_uuid)
        return plan_id, goal_id

async def safe_get_place_uuids(
    plan_short_uuid: str,
    place_short_uuid: str,
    user_id: int,
    get_chats_view: GetUserChatsView,
    get_places_view: GetPlacesView,
) -> tuple[UUID, UUID]:
    try:
        plan_id = get_full_uuid(plan_short_uuid)
        place_id = get_full_uuid(place_short_uuid)
        return plan_id, place_id
    except ValueError:
        await ensure_uuid_mapping_exists(user_id, get_chats_view)
        places_response = await get_places_view()
        for place in places_response.places:
            register_uuid_mapping(place.id)
        plan_id = get_full_uuid(plan_short_uuid)
        place_id = get_full_uuid(place_short_uuid)
        return plan_id, place_id

async def safe_get_exercise_uuids(
    plan_short_uuid: str,
    exercise_short_uuid: str,
    user_id: int,
    get_chats_view: GetUserChatsView,
    get_exercises_view: GetExercisesView,
) -> tuple[UUID, UUID]:
    try:
        plan_id = get_full_uuid(plan_short_uuid)
        exercise_id = get_full_uuid(exercise_short_uuid)
        return plan_id, exercise_id
    except ValueError:
        await ensure_uuid_mapping_exists(user_id, get_chats_view)
        exercises_response = await get_exercises_view()
        for exercise in exercises_response.exercises:
            register_uuid_mapping(exercise.id)
        plan_id = get_full_uuid(plan_short_uuid)
        exercise_id = get_full_uuid(exercise_short_uuid)
        return plan_id, exercise_id

@router.message(Command("start", "help"))
@inject
async def handle_start(
    message: types.Message,
    state: FSMContext,
    view: GetUserChatsView = Provide[DIContainer.get_user_chats_view],
) -> None:
    await FSMMainMenuManager.reset_main_menu_state(state)
    user_chats_response = await view(message.from_user.id)

    for chat in user_chats_response.chats:
        register_uuid_mapping(chat.id)
        register_uuid_mapping(chat.plan_id)

    keyboard = create_main_menu_keyboard(user_chats_response.chats)

    await message.answer(GREETINGS_MESSAGE, reply_markup=keyboard, user_id=message.from_user.id)

@router.callback_query(ChatAction.filter(F.action == "open"))
@inject
async def handle_open_chat(
    callback: types.CallbackQuery,
    callback_data: ChatAction,
    state: FSMContext,
    get_chats_view: GetUserChatsView = Provide[DIContainer.get_user_chats_view],
    get_plan_info_view: GetPlanInfoView = Provide[DIContainer.get_plan_info_view],
) -> None:
    try:
        chat_id = await safe_get_full_uuid(callback_data.chat_id, callback.from_user.id, get_chats_view)
    except ValueError:
        await callback.answer("Chat not found or link expired")
        return

    await state.update_data(active_chat_id=str(chat_id))

    user_chats_response = await get_chats_view(callback.from_user.id)

    try:
        current_chat = None
        for chat in user_chats_response.chats:
            if chat.id == chat_id:
                current_chat = chat
                break

        if current_chat is None:
            await callback.answer("Chat not found")
            return

        plan_info = await get_plan_info_view(current_chat.plan_id)

        await state.update_data(plan_id=str(current_chat.plan_id))

        is_complete = PlanFillingHelper.is_plan_complete(plan_info)
        has_description = plan_info.description is not None and len(plan_info.description.strip()) > 0
        plan_text = PlanFillingHelper.format_plan_info(plan_info)

        message_text = f"💬 Chat: {current_chat.name}\n\n{PLAN_INFO_MESSAGE.format(plan_info=plan_text)}"

        if is_complete:
            message_text += f"\n\n{PLAN_READY_MESSAGE}"
        else:
            message_text += f"\n\n{PLAN_EMPTY_MESSAGE}"

        keyboard = create_plan_keyboard(current_chat.plan_id, current_chat.id, is_complete, has_description)

        if callback.message:
            await callback.message.edit_text(message_text, reply_markup=keyboard)

    except Exception as e:
        await callback.answer(f"Error getting plan information: {str(e)}")
        return

    await callback.answer()

@router.callback_query(ChatAction.filter(F.action == "delete"))
@inject
async def handle_delete_chat(
    callback: types.CallbackQuery,
    callback_data: ChatAction,
    state: FSMContext,
    get_chats_view: GetUserChatsView = Provide[DIContainer.get_user_chats_view],
    delete_chat_view: DeleteChatView = Provide[DIContainer.delete_chat_view],
) -> None:
    try:
        chat_id = await safe_get_full_uuid(callback_data.chat_id, callback.from_user.id, get_chats_view)

        await delete_chat_view(chat_id)

        await FSMMainMenuManager.reset_main_menu_state(state)

        user_chats_response = await get_chats_view(callback.from_user.id)
        keyboard = create_main_menu_keyboard(user_chats_response.chats)

        if callback.message:
            await callback.message.edit_text(
                "✅ Chat deleted successfully!\n\n" + GREETINGS_MESSAGE, reply_markup=keyboard
            )

        await callback.answer("Chat deleted successfully!")

    except Exception as e:
        await callback.answer(f"Error deleting chat: {str(e)}")

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
        add_result = await add_chat_view(message.from_user.id, chat_name)
        user_chats_response = await get_chats_view(message.from_user.id)
        keyboard = create_main_menu_keyboard(user_chats_response.chats)

        await message.answer(
            f"{CHAT_CREATED_SUCCESS_MESSAGE.format(chat_name=chat_name)}\n\n{GREETINGS_MESSAGE}", reply_markup=keyboard
        )

        await FSMMainMenuManager.reset_main_menu_state(state)

    except Exception as e:
        await message.answer(ERROR_CHAT_CREATION_MESSAGE.format(error=str(e)))
        await FSMMainMenuManager.reset_main_menu_state(state)

        user_chats_response = await get_chats_view(message.from_user.id)
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

@router.callback_query(PlanAction.filter(F.action == "fill"))
@inject
async def handle_fill_plan(
    callback: types.CallbackQuery,
    callback_data: PlanAction,
    state: FSMContext,
    get_plan_info_view: GetPlanInfoView = Provide[DIContainer.get_plan_info_view],
    get_chats_view: GetUserChatsView = Provide[DIContainer.get_user_chats_view],
) -> None:
    try:
        plan_id = await safe_get_full_uuid(callback_data.plan_id, callback.from_user.id, get_chats_view)
        plan_info = await get_plan_info_view(plan_id)

        next_step = PlanFillingHelper.get_next_step(plan_info)

        if next_step == PlanFillingStates.choosing_factor.state:
            await start_factor_selection(callback, plan_id, state)
        elif next_step == PlanFillingStates.entering_disease.state:
            await start_disease_input(callback, state)
        elif next_step == PlanFillingStates.choosing_goal.state:
            await start_goal_selection(callback, plan_id, state)
        elif next_step == PlanFillingStates.choosing_place.state:
            await start_place_selection(callback, plan_id, state)
        elif next_step == PlanFillingStates.choosing_exercise.state:
            await start_exercise_selection(callback, plan_id, state)
        else:
            await callback.answer("Plan already completed!")

    except Exception as e:
        await callback.answer(f"Error: {str(e)}")

@inject
async def start_factor_selection(
    callback: types.CallbackQuery,
    plan_id: UUID,
    state: FSMContext,
    get_risk_factors_view: GetRiskFactorsView = Provide[DIContainer.get_risk_factors_view],
) -> None:
    try:
        factors_response = await get_risk_factors_view()

        for factor in factors_response.factors:
            register_uuid_mapping(factor.id)
        register_uuid_mapping(plan_id)

        keyboard = create_factors_keyboard(factors_response.factors, plan_id)

        await state.set_state(PlanFillingStates.choosing_factor)
        await state.update_data(plan_id=str(plan_id))

        if callback.message:
            await callback.message.edit_text(CHOOSE_RISK_FACTOR_MESSAGE, reply_markup=keyboard)

    except Exception as e:
        await callback.answer(f"Error getting risk factors: {str(e)}")

async def start_disease_input(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(PlanFillingStates.entering_disease)

    keyboard = create_disease_input_keyboard()

    if callback.message:
        await callback.message.edit_text(ENTER_DISEASE_MESSAGE, reply_markup=keyboard)

@inject
async def start_goal_selection(
    callback: types.CallbackQuery,
    plan_id: UUID,
    state: FSMContext,
    get_user_goals_view: GetUserGoalsView = Provide[DIContainer.get_user_goals_view],
) -> None:
    try:
        goals_response = await get_user_goals_view()

        for goal in goals_response.goals:
            register_uuid_mapping(goal.id)
        register_uuid_mapping(plan_id)

        keyboard = create_goals_keyboard(goals_response.goals, plan_id)

        await state.set_state(PlanFillingStates.choosing_goal)
        await state.update_data(plan_id=str(plan_id))

        if callback.message:
            await callback.message.edit_text(CHOOSE_GOAL_MESSAGE, reply_markup=keyboard)

    except Exception as e:
        await callback.answer(f"Error getting goals: {str(e)}")

@inject
async def start_place_selection(
    callback: types.CallbackQuery,
    plan_id: UUID,
    state: FSMContext,
    get_places_view: GetPlacesView = Provide[DIContainer.get_places_view],
) -> None:
    try:
        places_response = await get_places_view()

        for place in places_response.places:
            register_uuid_mapping(place.id)
        register_uuid_mapping(plan_id)

        keyboard = create_places_keyboard(places_response.places, plan_id)

        await state.set_state(PlanFillingStates.choosing_place)
        await state.update_data(plan_id=str(plan_id))

        if callback.message:
            await callback.message.edit_text(CHOOSE_PLACE_MESSAGE, reply_markup=keyboard)

    except Exception as e:
        await callback.answer(f"Error getting places: {str(e)}")

@inject
async def start_exercise_selection(
    callback: types.CallbackQuery,
    plan_id: UUID,
    state: FSMContext,
    get_exercises_view: GetExercisesView = Provide[DIContainer.get_exercises_view],
) -> None:
    try:
        exercises_response = await get_exercises_view()

        for exercise in exercises_response.exercises:
            register_uuid_mapping(exercise.id)
        register_uuid_mapping(plan_id)

        keyboard = create_exercises_keyboard(exercises_response.exercises, plan_id)

        await state.set_state(PlanFillingStates.choosing_exercise)
        await state.update_data(plan_id=str(plan_id))

        if callback.message:
            await callback.message.edit_text(CHOOSE_EXERCISE_MESSAGE, reply_markup=keyboard)

    except Exception as e:
        await callback.answer(f"Error getting exercises: {str(e)}")

@router.callback_query(FactorAction.filter())
@inject
async def handle_factor_selection(
    callback: types.CallbackQuery,
    callback_data: FactorAction,
    state: FSMContext,
    add_plan_factor_view: AddPlanFactorView = Provide[DIContainer.add_plan_factor_view],
    get_chats_view: GetUserChatsView = Provide[DIContainer.get_user_chats_view],
    get_risk_factors_view: GetRiskFactorsView = Provide[DIContainer.get_risk_factors_view],
    get_plan_info_view: GetPlanInfoView = Provide[DIContainer.get_plan_info_view],
) -> None:
    try:
        plan_id, factor_id = await safe_get_factor_uuids(
            callback_data.plan_id,
            callback_data.factor_id,
            callback.from_user.id,
            get_chats_view,
            get_risk_factors_view,
        )

        await add_plan_factor_view(plan_id, factor_id)
        await callback.answer(FACTOR_ADDED_MESSAGE)

        plan_info = await get_plan_info_view(plan_id)
        plan_text = PlanFillingHelper.format_plan_info(plan_info)
        
        if PlanFillingHelper.is_plan_complete(plan_info):
                plan_text = PlanFillingHelper.format_plan_info(plan_info)
            has_description = plan_info.description is not None and len(plan_info.description.strip()) > 0
            chat_id = await get_chat_id_by_plan_id(plan_id, callback.from_user.id, get_chats_view)

            message_text = (
                f"✅ Risk factor updated!\n\n{PLAN_INFO_MESSAGE.format(plan_info=plan_text)}\n\n{PLAN_READY_MESSAGE}"
            )
            keyboard = create_plan_keyboard(plan_id, chat_id, True, has_description)

            if callback.message:
                await callback.message.edit_text(message_text, reply_markup=keyboard)
            await FSMMainMenuManager.reset_main_menu_state(state)
        else:

            if callback.message:
                await callback.message.edit_text(
                    f"✅ {FACTOR_ADDED_MESSAGE}\n\n📋 Plan details:\n{plan_text}\n\n{ENTER_DISEASE_MESSAGE}",
                    reply_markup=create_disease_input_keyboard()
                )
            await state.set_state(PlanFillingStates.entering_disease)

    except Exception as e:
        await callback.answer(f"Error adding factor: {str(e)}")

@router.callback_query(Action.filter(F.action == SKIP_STEP))
@inject
async def handle_skip_disease(
    callback: types.CallbackQuery,
    callback_data: Action,
    state: FSMContext,
    add_plan_disease_view: AddPlanDiseaseView = Provide[DIContainer.add_plan_disease_view],
    get_user_goals_view: GetUserGoalsView = Provide[DIContainer.get_user_goals_view],
    get_plan_info_view: GetPlanInfoView = Provide[DIContainer.get_plan_info_view],
    get_chats_view: GetUserChatsView = Provide[DIContainer.get_user_chats_view],
) -> None:
    try:
        current_state = await state.get_state()
        if current_state != PlanFillingStates.entering_disease.state:
            await callback.answer("Skip is not available for this step")
            return

        data = await state.get_data()
        plan_id = UUID(data.get("plan_id"))

        await add_plan_disease_view(plan_id, "don't have")

        plan_info = await get_plan_info_view(plan_id)
        if PlanFillingHelper.is_plan_complete(plan_info):

            plan_text = PlanFillingHelper.format_plan_info(plan_info)
            has_description = plan_info.description is not None and len(plan_info.description.strip()) > 0
            chat_id = await get_chat_id_by_plan_id(plan_id, callback.from_user.id, get_chats_view)

            message_text = f"✅ Disease updated (skipped)!\n\n{PLAN_INFO_MESSAGE.format(plan_info=plan_text)}\n\n{PLAN_READY_MESSAGE}"
            keyboard = create_plan_keyboard(plan_id, chat_id, True, has_description)

            if callback.message:
                await callback.message.edit_text(message_text, reply_markup=keyboard)
            await FSMMainMenuManager.reset_main_menu_state(state)
        else:

            goals_response = await get_user_goals_view()

            for goal in goals_response.goals:
                register_uuid_mapping(goal.id)
            register_uuid_mapping(plan_id)

            keyboard = create_goals_keyboard(goals_response.goals, plan_id)

            await state.set_state(PlanFillingStates.choosing_goal)

            if callback.message:
                await callback.message.edit_text(
                    f"{STEP_SKIPPED_MESSAGE}\n\n{CHOOSE_GOAL_MESSAGE}", reply_markup=keyboard
                )

        await callback.answer()

    except Exception as e:
        await callback.answer(f"Error skipping disease step: {str(e)}")

@router.message(PlanFillingStates.entering_disease)
@inject
async def handle_disease_input(
    message: types.Message,
    state: FSMContext,
    add_plan_disease_view: AddPlanDiseaseView = Provide[DIContainer.add_plan_disease_view],
    get_user_goals_view: GetUserGoalsView = Provide[DIContainer.get_user_goals_view],
    get_plan_info_view: GetPlanInfoView = Provide[DIContainer.get_plan_info_view],
    get_chats_view: GetUserChatsView = Provide[DIContainer.get_user_chats_view],
) -> None:
    if not message.text:
        await message.answer(ERROR_TEXT_ONLY_MESSAGE)
        return

    disease_name = message.text.strip()
    if not disease_name:
        await message.answer(ERROR_EMPTY_DISEASE_NAME)
        return

    try:
        data = await state.get_data()
        plan_id = UUID(data.get("plan_id"))

        await add_plan_disease_view(plan_id, disease_name)

        plan_info = await get_plan_info_view(plan_id)
        plan_text = PlanFillingHelper.format_plan_info(plan_info)
        
        if PlanFillingHelper.is_plan_complete(plan_info):

            plan_text = PlanFillingHelper.format_plan_info(plan_info)
            has_description = plan_info.description is not None and len(plan_info.description.strip()) > 0
            chat_id = await get_chat_id_by_plan_id(plan_id, message.from_user.id, get_chats_view)

            message_text = (
                f"✅ Disease updated!\n\n{PLAN_INFO_MESSAGE.format(plan_info=plan_text)}\n\n{PLAN_READY_MESSAGE}"
            )
            keyboard = create_plan_keyboard(plan_id, chat_id, True, has_description)

            await message.answer(message_text, reply_markup=keyboard)
            await FSMMainMenuManager.reset_main_menu_state(state)
        else:

            goals_response = await get_user_goals_view()

            for goal in goals_response.goals:
                register_uuid_mapping(goal.id)
            register_uuid_mapping(plan_id)

            keyboard = create_goals_keyboard(goals_response.goals, plan_id)

            await state.set_state(PlanFillingStates.choosing_goal)

            await message.answer(
                f"✅ {DISEASE_ADDED_MESSAGE}\n\n📋 Plan details:\n{plan_text}\n\n{CHOOSE_GOAL_MESSAGE}",
                reply_markup=keyboard
            )

    except Exception as e:
        await message.answer(f"Error adding disease: {str(e)}")

@router.callback_query(GoalAction.filter())
@inject
async def handle_goal_selection(
    callback: types.CallbackQuery,
    callback_data: GoalAction,
    state: FSMContext,
    add_plan_goal_view: AddPlanGoalView = Provide[DIContainer.add_plan_goal_view],
    get_chats_view: GetUserChatsView = Provide[DIContainer.get_user_chats_view],
    get_user_goals_view: GetUserGoalsView = Provide[DIContainer.get_user_goals_view],
    get_plan_info_view: GetPlanInfoView = Provide[DIContainer.get_plan_info_view],
    get_places_view: GetPlacesView = Provide[DIContainer.get_places_view],
) -> None:
    try:
        plan_id, goal_id = await safe_get_goal_uuids(
            callback_data.plan_id,
            callback_data.goal_id,
            callback.from_user.id,
            get_chats_view,
            get_user_goals_view,
        )

        await add_plan_goal_view(plan_id, goal_id)
        await callback.answer(GOAL_ADDED_MESSAGE)

        plan_info = await get_plan_info_view(plan_id)
        plan_text = PlanFillingHelper.format_plan_info(plan_info)
        
        if PlanFillingHelper.is_plan_complete(plan_info):

            plan_text = PlanFillingHelper.format_plan_info(plan_info)
            has_description = plan_info.description is not None and len(plan_info.description.strip()) > 0
            chat_id = await get_chat_id_by_plan_id(plan_id, callback.from_user.id, get_chats_view)

            message_text = (
                f"✅ Goal updated!\n\n{PLAN_INFO_MESSAGE.format(plan_info=plan_text)}\n\n{PLAN_READY_MESSAGE}"
            )
            keyboard = create_plan_keyboard(plan_id, chat_id, True, has_description)

            if callback.message:
                await callback.message.edit_text(message_text, reply_markup=keyboard)
            await FSMMainMenuManager.reset_main_menu_state(state)
        else:

            places_response = await get_places_view()
            for place in places_response.places:
                register_uuid_mapping(place.id)

            if callback.message:
                await callback.message.edit_text(
                    f"✅ {GOAL_ADDED_MESSAGE}\n\n📋 Plan details:\n{plan_text}\n\n{CHOOSE_PLACE_MESSAGE}",
                    reply_markup=create_places_keyboard(places_response.places, plan_id)
                )
            await state.set_state(PlanFillingStates.choosing_place)

    except Exception as e:
        await callback.answer(f"Error adding goal: {str(e)}")

@router.callback_query(PlaceAction.filter())
@inject
async def handle_place_selection(
    callback: types.CallbackQuery,
    callback_data: PlaceAction,
    state: FSMContext,
    add_plan_place_view: AddPlanPlaceView = Provide[DIContainer.add_plan_place_view],
    get_chats_view: GetUserChatsView = Provide[DIContainer.get_user_chats_view],
    get_places_view: GetPlacesView = Provide[DIContainer.get_places_view],
    get_plan_info_view: GetPlanInfoView = Provide[DIContainer.get_plan_info_view],
    get_exercises_view: GetExercisesView = Provide[DIContainer.get_exercises_view],
) -> None:
    try:
        plan_id, place_id = await safe_get_place_uuids(
            callback_data.plan_id,
            callback_data.place_id,
            callback.from_user.id,
            get_chats_view,
            get_places_view,
        )

        await add_plan_place_view(plan_id, place_id)
        await callback.answer(PLACE_ADDED_MESSAGE)

        plan_info = await get_plan_info_view(plan_id)
        plan_text = PlanFillingHelper.format_plan_info(plan_info)
        
        if PlanFillingHelper.is_plan_complete(plan_info):

            plan_text = PlanFillingHelper.format_plan_info(plan_info)
            has_description = plan_info.description is not None and len(plan_info.description.strip()) > 0
            chat_id = await get_chat_id_by_plan_id(plan_id, callback.from_user.id, get_chats_view)

            message_text = (
                f"✅ Place updated!\n\n{PLAN_INFO_MESSAGE.format(plan_info=plan_text)}\n\n{PLAN_READY_MESSAGE}"
            )
            keyboard = create_plan_keyboard(plan_id, chat_id, True, has_description)

            if callback.message:
                await callback.message.edit_text(message_text, reply_markup=keyboard)
            await FSMMainMenuManager.reset_main_menu_state(state)
        else:

            exercises_response = await get_exercises_view()
            for exercise in exercises_response.exercises:
                register_uuid_mapping(exercise.id)

            if callback.message:
                await callback.message.edit_text(
                    f"✅ {PLACE_ADDED_MESSAGE}\n\n📋 Plan details:\n{plan_text}\n\n{CHOOSE_EXERCISE_MESSAGE}",
                    reply_markup=create_exercises_keyboard(exercises_response.exercises, plan_id)
                )
            await state.set_state(PlanFillingStates.choosing_exercise)

    except Exception as e:
        await callback.answer(f"Error adding place: {str(e)}")

@router.callback_query(ExerciseAction.filter())
@inject
async def handle_exercise_selection(
    callback: types.CallbackQuery,
    callback_data: ExerciseAction,
    state: FSMContext,
    add_plan_exercise_view: AddPlanExerciseView = Provide[DIContainer.add_plan_exercise_view],
    get_plan_info_view: GetPlanInfoView = Provide[DIContainer.get_plan_info_view],
    get_chats_view: GetUserChatsView = Provide[DIContainer.get_user_chats_view],
    get_exercises_view: GetExercisesView = Provide[DIContainer.get_exercises_view],
) -> None:
    try:

        plan_id, exercise_id = await safe_get_exercise_uuids(
            callback_data.plan_id,
            callback_data.exercise_id,
            callback.from_user.id,
            get_chats_view,
            get_exercises_view,
        )

        old_plan_info = await get_plan_info_view(plan_id)
        was_complete = PlanFillingHelper.is_plan_complete(old_plan_info)

        await add_plan_exercise_view(plan_id, exercise_id)
        await callback.answer(EXERCISE_ADDED_MESSAGE)

        plan_info = await get_plan_info_view(plan_id)
        plan_text = PlanFillingHelper.format_plan_info(plan_info)
        chat_id = await get_chat_id_by_plan_id(plan_id, callback.from_user.id, get_chats_view)

        if was_complete:

            has_description = plan_info.description is not None and len(plan_info.description.strip()) > 0
            message_text = (
                f"✅ Exercise updated!\n\n{PLAN_INFO_MESSAGE.format(plan_info=plan_text)}\n\n{PLAN_READY_MESSAGE}"
            )
            keyboard = create_plan_keyboard(plan_id, chat_id, True, has_description)
            await FSMMainMenuManager.reset_main_menu_state(state)
        else:

            message_text = f"🎉 Plan completed successfully!\n\n{PLAN_INFO_MESSAGE.format(plan_info=plan_text)}\n\n{PLAN_READY_MESSAGE}"
            keyboard = create_plan_keyboard(plan_id, chat_id, True, False)
            await state.set_state(PlanFillingStates.plan_completed)

        if callback.message:
            await callback.message.edit_text(message_text, reply_markup=keyboard)

    except Exception as e:
        await callback.answer(f"Error adding exercise: {str(e)}")

@router.callback_query(PlanAction.filter(F.action == "generate_recommendations"))
@inject
async def handle_generate_recommendations(
    callback: types.CallbackQuery,
    callback_data: PlanAction,
    state: FSMContext,
    generate_plan_view: GeneratePlanView = Provide[DIContainer.generate_plan_view],
    get_plan_info_view: GetPlanInfoView = Provide[DIContainer.get_plan_info_view],
    get_chats_view: GetUserChatsView = Provide[DIContainer.get_user_chats_view],
) -> None:
    try:
        plan_id = await safe_get_full_uuid(callback_data.plan_id, callback.from_user.id, get_chats_view)

        plan_info = await get_plan_info_view(plan_id)
        if not PlanFillingHelper.is_plan_complete(plan_info):
            await callback.answer("Please complete the entire plan first!")
            return

        if callback.message:
            await callback.message.edit_text(GENERATING_RECOMMENDATIONS_MESSAGE)

        had_description = plan_info.description is not None and len(plan_info.description.strip()) > 0
        result = await generate_plan_view(plan_id)

        updated_plan_info = await get_plan_info_view(plan_id)
        plan_text = PlanFillingHelper.format_plan_info(updated_plan_info)

        if had_description:
            success_message = RECOMMENDATIONS_UPDATED_MESSAGE
        else:
            success_message = RECOMMENDATIONS_GENERATED_MESSAGE

        message_text = f"{success_message}\n\n{PLAN_INFO_MESSAGE.format(plan_info=plan_text)}"

        chat_id = await get_chat_id_by_plan_id(plan_id, callback.from_user.id, get_chats_view)
        keyboard = create_plan_keyboard(plan_id, chat_id, True, True)

        if callback.message:
            await callback.message.edit_text(message_text, reply_markup=keyboard)

        await callback.answer("Done!")

    except Exception as e:
        await callback.answer(f"Error generating recommendations: {str(e)}")
        try:
            plan_info = await get_plan_info_view(plan_id)
            plan_text = PlanFillingHelper.format_plan_info(plan_info)
            is_complete = PlanFillingHelper.is_plan_complete(plan_info)
            has_description = plan_info.description is not None and len(plan_info.description.strip()) > 0

            message_text = f"{PLAN_INFO_MESSAGE.format(plan_info=plan_text)}"
            if is_complete:
                message_text += f"\n\n{PLAN_READY_MESSAGE}"

            chat_id = await get_chat_id_by_plan_id(plan_id, callback.from_user.id, get_chats_view)
            keyboard = create_plan_keyboard(plan_id, chat_id, is_complete, has_description)
            if callback.message:
                await callback.message.edit_text(message_text, reply_markup=keyboard)
        except:
            pass

@router.callback_query(PlanAction.filter(F.action == "update_recommendations"))
@inject
async def handle_update_recommendations(
    callback: types.CallbackQuery,
    callback_data: PlanAction,
    state: FSMContext,
    get_plan_info_view: GetPlanInfoView = Provide[DIContainer.get_plan_info_view],
    get_chats_view: GetUserChatsView = Provide[DIContainer.get_user_chats_view],
) -> None:
    try:
        plan_id = await safe_get_full_uuid(callback_data.plan_id, callback.from_user.id, get_chats_view)

        plan_info = await get_plan_info_view(plan_id)
        if not PlanFillingHelper.is_plan_complete(plan_info):
            await callback.answer("Please complete the entire plan first!")
            return

        if not (plan_info.description and len(plan_info.description.strip()) > 0):
            await callback.answer("Plan must have recommendations to update them!")
            return

        await state.update_data(plan_id=str(plan_id))
        await state.set_state(UpdatePlanStates.waiting_for_preferences)

        keyboard = create_preferences_input_keyboard()

        if callback.message:
            await callback.message.edit_text(ENTER_PREFERENCES_MESSAGE, reply_markup=keyboard)

        await callback.answer()

    except Exception as e:
        await callback.answer(f"Error: {str(e)}")

@router.message(UpdatePlanStates.waiting_for_preferences)
@inject
async def handle_preferences_input(
    message: types.Message,
    state: FSMContext,
    update_plan_view: UpdatePlanView = Provide[DIContainer.update_plan_view],
    get_plan_info_view: GetPlanInfoView = Provide[DIContainer.get_plan_info_view],
    get_chats_view: GetUserChatsView = Provide[DIContainer.get_user_chats_view],
) -> None:
    if not message.text:
        await message.answer(ERROR_TEXT_ONLY_MESSAGE)
        return

    preferences = message.text.strip()
    if not preferences:
        await message.answer(ERROR_EMPTY_PREFERENCES_MESSAGE)
        return

    try:
        data = await state.get_data()
        plan_id = UUID(data.get("plan_id"))

        processing_msg = await message.answer(UPDATING_PLAN_MESSAGE)

        result = await update_plan_view(plan_id, preferences)

        updated_plan_info = await get_plan_info_view(plan_id)
        plan_text = PlanFillingHelper.format_plan_info(updated_plan_info)

        message_text = f"{PLAN_UPDATED_SUCCESS_MESSAGE}\n\n{PLAN_INFO_MESSAGE.format(plan_info=plan_text)}"

        chat_id = await get_chat_id_by_plan_id(plan_id, message.from_user.id, get_chats_view)
        keyboard = create_plan_keyboard(plan_id, chat_id, True, True)

        await processing_msg.delete()
        await message.answer(message_text, reply_markup=keyboard)

        await state.clear()

    except Exception as e:
        await message.answer(f"Error updating plan: {str(e)}")
        await FSMMainMenuManager.reset_main_menu_state(state)

@router.callback_query(PlanAction.filter(F.action == "edit_risk_factor"))
@inject
async def handle_edit_risk_factor(
    callback: types.CallbackQuery,
    callback_data: PlanAction,
    state: FSMContext,
    get_chats_view: GetUserChatsView = Provide[DIContainer.get_user_chats_view],
) -> None:
    try:
        plan_id = await safe_get_full_uuid(callback_data.plan_id, callback.from_user.id, get_chats_view)
        await start_factor_selection(callback, plan_id, state)
        await callback.answer()
    except Exception as e:
        await callback.answer(f"Error: {str(e)}")

@router.callback_query(PlanAction.filter(F.action == "edit_disease"))
@inject
async def handle_edit_disease(
    callback: types.CallbackQuery,
    callback_data: PlanAction,
    state: FSMContext,
    get_chats_view: GetUserChatsView = Provide[DIContainer.get_user_chats_view],
) -> None:
    try:
        plan_id = await safe_get_full_uuid(callback_data.plan_id, callback.from_user.id, get_chats_view)
        await state.update_data(plan_id=str(plan_id))
        await start_disease_input(callback, state)
        await callback.answer()
    except Exception as e:
        await callback.answer(f"Error: {str(e)}")

@router.callback_query(PlanAction.filter(F.action == "edit_goal"))
@inject
async def handle_edit_goal(
    callback: types.CallbackQuery,
    callback_data: PlanAction,
    state: FSMContext,
    get_chats_view: GetUserChatsView = Provide[DIContainer.get_user_chats_view],
) -> None:
    try:
        plan_id = await safe_get_full_uuid(callback_data.plan_id, callback.from_user.id, get_chats_view)
        await start_goal_selection(callback, plan_id, state)
        await callback.answer()
    except Exception as e:
        await callback.answer(f"Error: {str(e)}")

@router.callback_query(PlanAction.filter(F.action == "edit_place"))
@inject
async def handle_edit_place(
    callback: types.CallbackQuery,
    callback_data: PlanAction,
    state: FSMContext,
    get_chats_view: GetUserChatsView = Provide[DIContainer.get_user_chats_view],
) -> None:
    try:
        plan_id = await safe_get_full_uuid(callback_data.plan_id, callback.from_user.id, get_chats_view)
        await start_place_selection(callback, plan_id, state)
        await callback.answer()
    except Exception as e:
        await callback.answer(f"Error: {str(e)}")

@router.callback_query(PlanAction.filter(F.action == "edit_exercise"))
@inject
async def handle_edit_exercise(
    callback: types.CallbackQuery,
    callback_data: PlanAction,
    state: FSMContext,
    get_chats_view: GetUserChatsView = Provide[DIContainer.get_user_chats_view],
) -> None:
    try:
        plan_id = await safe_get_full_uuid(callback_data.plan_id, callback.from_user.id, get_chats_view)
        await start_exercise_selection(callback, plan_id, state)
        await callback.answer()
    except Exception as e:
        await callback.answer(f"Error: {str(e)}")

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
