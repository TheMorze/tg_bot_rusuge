from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, \
                                   ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from database.service import Database
from keyboards.create_reply_kb import create_reply_keyboard
from keyboards.menu_keyboard import menu_keyboard
from FSM.state import FSMStresses
from lexicon.lexicon import LEXICON_RU

# Инициализация роутера уровня модуля
router = Router()

@router.message(CommandStart())
async def process_start_command(message: Message):
    Database.set_user(user_id=message.from_user.id, user_name=message.from_user.username)
    await message.answer(
        text=LEXICON_RU['/start'],
        reply_markup=menu_keyboard
    )
    
@router.message(Command(commands=['menu']))
async def process_menu_command(message: Message):
    await message.answer(
            text=LEXICON_RU['/menu'],
            reply_markup=menu_keyboard
        )
    
@router.message(F.text.lower() == '🥷 практиковаться', StateFilter(default_state))
async def process_practice_command(message: Message, state: FSMContext):
    await state.set_state(FSMStresses.in_choosing)
    
    keyboard = create_reply_keyboard(width=3, resize_keyboard=True, args={'🎯 Ударения'})
    await message.answer(
        text='Что будем практиковать в этот раз?',
        reply_markup=keyboard
    )
    
@router.message(Command('help'))
async def process_help_command(message: Message):
    await message.answer(
        text=LEXICON_RU['/help'],
        reply_markup=menu_keyboard
    )
    
@router.message(F.text.lower().in_(['/stats', '📊 статистика']), StateFilter(default_state))
async def process_stats_command(message: Message):
    user_id = message.from_user.id
    
    score = Database.get_user_score(user_id=user_id)
    correct = Database.get_user_correct(user_id=user_id)
    not_correct = Database.get_user_not_correct(user_id=user_id)
    
    await message.reply(text=LEXICON_RU['/stats'].format(score=score, correct=correct, not_correct=not_correct),
                        reply_markup=menu_keyboard)
    
@router.message(Command('cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text=LEXICON_RU['impossible_cancel']
    )