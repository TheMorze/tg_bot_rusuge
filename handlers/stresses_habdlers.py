from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, \
                          ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from lexicon.lexicon import LEXICON_RU
from lexicon.stresses import STRESSES
from extra_funcs.stresses_processing import choose_random_stress

router = Router()

kb_builder = ReplyKeyboardBuilder()

@router.message(lambda msg: msg.text in ('🎯 Ударения', LEXICON_RU['correct'], LEXICON_RU['not_correct']))
async def process_stress_tasks(message: Message):
    word, options = choose_random_stress()
    buttons = [
        KeyboardButton(text=option) for option in options
    ]
    kb_builder.row(*buttons)
    print(stack)
    await message.answer(
        text=word,
        reply_markup=kb_builder.as_markup(resize_keyboard=True)
    )
    
@router.message(lambda msg: msg.text in stack[-1])
async def process_answer_task(message: Message):
    if message.text == stack[-2]:
        await message.answer(
            text=LEXICON_RU['correct']
        )
    else:
        await message.answer(
            text=LEXICON_RU['not_correct']
        )