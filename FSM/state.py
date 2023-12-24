from aiogram.fsm.state import State, StatesGroup

class FSMPracticing(StatesGroup):
    in_choosing_practice = State()
    in_choosing_prototypes = State()
    
    stresses = State()
    prototypes = State()