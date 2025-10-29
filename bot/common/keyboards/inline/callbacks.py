from typing import Optional
from uuid import UUID

from aiogram.filters.callback_data import CallbackData

_uuid_mapping: dict[str, UUID] = {}
_reverse_mapping: dict[UUID, str] = {}

def shorten_uuid(uuid: UUID) -> str:
    return str(uuid)[:5]

def register_uuid_mapping(uuid: UUID) -> str:
    short = shorten_uuid(uuid)
    _uuid_mapping[short] = uuid
    _reverse_mapping[uuid] = short
    return short

def get_full_uuid(short_uuid: str) -> UUID:
    if short_uuid in _uuid_mapping:
        return _uuid_mapping[short_uuid]
    raise ValueError(f"UUID with short ID {short_uuid} not found in mapping")

class Action(CallbackData, prefix="act"):
    action: str

class ChatAction(CallbackData, prefix="chat"):
    action: str
    chat_id: str

class PlanAction(CallbackData, prefix="plan"):
    action: str
    plan_id: str

class FactorAction(CallbackData, prefix="factor"):
    factor_id: str
    plan_id: str

class GoalAction(CallbackData, prefix="goal"):
    goal_id: str
    plan_id: str

class PlaceAction(CallbackData, prefix="place"):
    place_id: str
    plan_id: str

class ExerciseAction(CallbackData, prefix="exercise"):
    exercise_id: str
    plan_id: str

class ExerciseTypeAction(CallbackData, prefix="exercise_type"):
    type: str
    plan_id: str
