import random
from loguru import logger

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from lexicon.lexicon import LEXICON_RU, PROTOTYPES
from FSM.state import FSMPracticing
from database.prototypes import Prototype

from keyboards.menu_keyboard import get_menu_keyboard
from extra_funcs.answers_processing import update_stats
from keyboards.inline_keyboards import get_portions

from filters.prototypes_filters import AnswerFromalization

router = Router()

@router.callback_query(F.data.startswith('prototype'), StateFilter(FSMPracticing.in_choosing_prototypes))
async def choose_portion(callback: CallbackQuery, state: FSMContext):
    prototype = callback.data
    await state.update_data(prototype=prototype)
    
    await callback.message.edit_text(text=LEXICON_RU['topic_chosen'].format(topic=PROTOTYPES[callback.data]))
    await callback.message.edit_reply_markup(reply_markup=get_portions())

@router.callback_query(F.data.startswith('portion'), StateFilter(FSMPracticing.in_choosing_prototypes))
async def start_prototypes(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    prototype_name = data['prototype']
    prototype = int(prototype_name.split('_')[1])
    
    limit = int(callback.data.split('_')[1])
    
    tasks = Prototype.get_random_tasks(prototype=prototype)
    text, source, correct = tasks[0]
    
    await state.update_data(correct=correct, tasks=tasks,
                            i=1, user_correct=0, user_incorrect=0,
                            prototype=prototype, limit=limit)

    await state.set_state(FSMPracticing.prototypes)
    
    await callback.message.edit_text(text=LEXICON_RU['portion_chosen'].format(topic=PROTOTYPES[prototype_name],
                                                                        limit=limit))
    await callback.message.answer(
            text=f'<b><i>Введите в чат ответ на вопрос</i></b>\n\n'
                 f'{text}\n\n'
                 f'<i>Источник:</i> <b>{source}</b>'
        )
    
    await callback.answer()
    
@router.message(AnswerFromalization(task_type='prototypes'), StateFilter(FSMPracticing.prototypes))
async def process_prototypes_tasks(message: Message, state: FSMContext):
    data = await state.get_data()
    correct, tasks, i = data['correct'], data['tasks'], data['i']
    prototype = data['prototype']
    limit = data['limit']
    user_correct, user_incorrect = data['user_correct'], data['user_incorrect']
    if sorted(message.text) == sorted(str(correct)):
        user_correct += 1
        await state.update_data(user_correct=user_correct)
        await message.answer(text=LEXICON_RU['correct'].format(answer=str(correct)))
    else:
        user_incorrect += 1
        await state.update_data(user_incorrect=user_incorrect)
        await message.answer(text=LEXICON_RU['not_correct'].format(answer=str(correct)))
    

    # Отправляем пользователю новый таск и перемешиваем варианты
    if i < limit:
        text, source, correct = tasks[i]
        
        await state.update_data(correct=correct, i=i + 1)
        await message.answer(
            text=f'<b><i>Введите в чат ответ на вопрос</i></b>\n\n'
                 f'{text}\n\n'
                 f'<i>Источник:</i> <b>{source}</b>'
        )
        
    else:
        await update_stats(user_id=message.from_user.id,
                     topic_name=f'prototype_{prototype}',
                     user_correct=user_correct,
                     user_incorrect=user_incorrect)
        
        await message.answer(text=LEXICON_RU['bye'].format(user_correct=user_correct,
                                                            user_incorrect=user_incorrect))
        await state.clear()
        
@router.message(Command(commands='cancel'), StateFilter(FSMPracticing.prototypes))
async def process_cancel_practicing(message: Message, state: FSMContext):
    data = await state.get_data()
    user_correct, user_incorrect = data['user_correct'], data['user_incorrect']
    prototype = data['prototype']
    
    await update_stats(user_id=message.from_user.id,
                     topic_name=f'prototype_{prototype}',
                     user_correct=user_correct,
                     user_incorrect=user_incorrect)
    
    await state.clear()
    await message.answer(text=LEXICON_RU['bye'].format(user_correct=user_correct,
                                                       user_incorrect=user_incorrect),
                         reply_markup=get_menu_keyboard())
        
@router.message(StateFilter(FSMPracticing.prototypes))
async def process_others_practicing(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['incorrect_formalization'])
    