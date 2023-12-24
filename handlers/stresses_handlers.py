import random

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from lexicon.lexicon import LEXICON_RU
from FSM.state import FSMPracticing
from database.users import Users
from database.practice import Stresses

from extra_funcs.answers_processing import update_stats
from keyboards.create_reply_kb import create_reply_keyboard
from keyboards.menu_keyboard import get_menu_keyboard
from keyboards.inline_keyboards import get_portions

router = Router()

@router.callback_query(F.data == 'stresses', StateFilter(FSMPracticing.in_choosing_practice))
async def choose_portion(callback: CallbackQuery, state: StateFilter):
    await callback.message.edit_text(text=LEXICON_RU['topic_chosen'].format(topic='🎯 Ударения'))
    await callback.message.edit_reply_markup(reply_markup=get_portions())

@router.callback_query(F.data.startswith('portion'), StateFilter(FSMPracticing.in_choosing_practice))
async def start_practice_stresses(callback: CallbackQuery, state: FSMContext):
    limit = int(callback.data.split('_')[1])
    
    words = Stresses.get_random_words()
    word, options, correct = words[0]
    options = options.split(',')
    random.shuffle(options)
    
    keyboard = create_reply_keyboard(width=5, resize_keyboard=True, args=options)

    await state.update_data(correct=correct, options=options,
                            words=words, i=1, user_correct=0, user_incorrect=0,
                            limit=limit)
    
    await state.set_state(FSMPracticing.stresses)
            
    await callback.message.edit_text(text=LEXICON_RU['portion_chosen'].format(topic='🎯 Ударения',
                                                                              limit=limit))
    await callback.message.answer(
            text=f'Выберите правильное ударение:\n\n<b>{word}</b>',
            reply_markup=keyboard
        )
    
    await callback.answer()

# Хэндлер для обработки ответов ударений
@router.message(F.text.isalpha(), \
                StateFilter(FSMPracticing.stresses))
async def process_stress_tasks(message: Message, state: FSMContext):
    data = await state.get_data()
    correct, options, words, i = data['correct'], data['options'], data['words'], data['i']
    user_correct, user_incorrect = data['user_correct'], data['user_incorrect']
    limit = data['limit']
    if message.text in options:
        if message.text == correct:
            user_correct += 1
            await state.update_data(user_correct=user_correct)
            await message.answer(text=LEXICON_RU['correct'].format(answer=str(correct)))
        else:
            user_incorrect += 1
            await state.update_data(user_incorrect=user_incorrect)
            await message.answer(text=LEXICON_RU['not_correct'].format(answer=str(correct)))
        

        # Отправляем пользователю новый таск и перемешиваем варианты
        if i < limit:
            word, options, correct = words[i]
            options = options.split(',')
            random.shuffle(options)
        
            keyboard = create_reply_keyboard(width=5, resize_keyboard=True, args=options)
            
            await state.update_data(correct=correct, options=options, i=i + 1)
            await message.answer(
                text=f'Выберите правильное ударение:\n\n<b>{word}</b>',
                reply_markup=keyboard
            )
        else:
            await update_stats(user_id=message.from_user.id,
                            topic_name=f'stresses',
                            user_correct=user_correct,
                            user_incorrect=user_incorrect)
            
            await message.answer(text=LEXICON_RU['bye'].format(user_correct=user_correct,
                                                               user_incorrect=user_incorrect),
                                 reply_markup=get_menu_keyboard())
            await state.clear()
        
    else:
        await message.answer(text=LEXICON_RU['not_stated_practicing'])
    
@router.message(Command(commands='cancel'), StateFilter(FSMPracticing.stresses))
async def process_cancel_practicing(message: Message, state: FSMContext):
    data = await state.get_data()
    user_correct, user_incorrect = data['user_correct'], data['user_incorrect']
    
    await update_stats(user_id=message.from_user.id,
                     topic_name=f'stresses',
                     user_correct=user_correct,
                     user_incorrect=user_incorrect)
    
    await state.clear()
    await message.answer(text=LEXICON_RU['bye'].format(user_correct=user_correct,
                                                       user_incorrect=user_incorrect),
                         reply_markup=get_menu_keyboard())
    
@router.message(StateFilter(FSMPracticing.stresses))
async def process_others_practicing(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['not_stated_practicing'])
    