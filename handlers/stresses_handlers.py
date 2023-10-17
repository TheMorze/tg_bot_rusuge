from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from lexicon.lexicon import LEXICON_RU
from lexicon.stresses import STRESSES
from FSM.state import FSMStresses
from database.service import Database

from extra_funcs.stresses_processing import choose_random_stress, process_correct, \
                                            process_not_correct
from keyboards.create_reply_kb import create_reply_keyboard
from keyboards.menu_keyboard import menu_keyboard

router = Router()

# Хэндлер для запуска практики ударений, 
# если пользователь в дефолтном состоянии
@router.message(F.text == '🎯 Ударения', StateFilter(FSMStresses.in_choosing))
async def start_practice_stresses(message: Message, state: FSMContext):
    word, options, correct = choose_random_stress()
    keyboard = create_reply_keyboard(width=5, resize_keyboard=True, args=options)

    await state.update_data(correct=correct, options=options)
    await state.set_state(FSMStresses.in_practicing)
    await message.answer(
            text=f'Выберите правильное ударение:\n\n<b>{word}</b>',
            reply_markup=keyboard
        )

# Хэндлер для обработки ответов ударений
@router.message(F.text.isalpha(), \
                StateFilter(FSMStresses.in_practicing))
async def process_stress_tasks(message: Message, state: FSMContext):
    data = await state.get_data()
    correct, options = data['correct'], data['options']
    if message.text in options:
        if message.text == correct:
            process_correct(user_id=message.from_user.id)
            await message.answer(text=LEXICON_RU['correct'])
        else:
            process_not_correct(user_id=message.from_user.id)
            await message.answer(text=LEXICON_RU['not_correct'])

        # Отправляем пользователю новый таск
        word, options, correct = choose_random_stress()
        keyboard = create_reply_keyboard(width=5, resize_keyboard=True, args=options)
        
        await state.update_data(correct=correct, options=options)
        await message.answer(
            text=f'Выберите правильное ударение:\n\n<b>{word}</b>',
            reply_markup=keyboard
        )
        
    else:
        await message.answer(text=LEXICON_RU['not_stated_practicing'])
    
@router.message(Command(commands='cancel'), StateFilter(FSMStresses.in_practicing))
async def process_cancel_practicing(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=LEXICON_RU['bye'], reply_markup=menu_keyboard)
    
@router.message(StateFilter(FSMStresses.in_practicing))
async def process_others_practicing(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['not_stated_practicing'])
    