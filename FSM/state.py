from aiogram.fsm.state import State, StatesGroup

class FSMStresses(StatesGroup):
    in_choosing = State()
    in_practicing = State()