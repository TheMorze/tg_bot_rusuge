from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, \
                                   ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from database.users import Users
from database.user_stats import UserStats
from keyboards.create_reply_kb import create_reply_keyboard
from keyboards.menu_keyboard import get_menu_keyboard
from keyboards.inline_keyboards import get_settings_keyboard, get_statistics_keyboard, \
                                       get_practice_list, get_solving_list
                                    
from FSM.state import FSMPracticing
from lexicon.lexicon import LEXICON_RU

# Инициализация роутера уровня модуля
router = Router()

@router.message(CommandStart(), \
    ~StateFilter(FSMPracticing.stresses, FSMPracticing.prototypes))
async def process_start_command(message: Message):
    user_id = message.from_user.id
    Users.set_user(user_id=user_id,
                   user_name=message.from_user.username)
    UserStats.set_user_stats(user_id=user_id)
    
    await message.answer(
        text=LEXICON_RU['/start'],
        reply_markup=get_menu_keyboard()
    )
    
@router.message(Command(commands=['menu']), \
    ~StateFilter(FSMPracticing.stresses, FSMPracticing.prototypes))
async def process_menu_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
            text=LEXICON_RU['/menu'],
            reply_markup=get_menu_keyboard()
        )
    
@router.message(F.text.lower() == '🥷 практиковаться', \
    ~StateFilter(FSMPracticing.stresses, FSMPracticing.prototypes))
async def process_practice_command(message: Message, state: FSMContext):
    await state.set_state(FSMPracticing.in_choosing_practice)
    
    await message.answer(
        text='Выбери раздел из нижепредставленных:',
        reply_markup=get_practice_list()
    )
    
@router.message(F.text.lower() == '💡 решать прототипы', \
            ~StateFilter(FSMPracticing.stresses, FSMPracticing.prototypes))
async def process_solving_command(message: Message, state: FSMContext):
    await state.set_state(FSMPracticing.in_choosing_prototypes)
    
    await message.answer(
        text='Выбери раздел из нижепредставленных:',
        reply_markup=get_solving_list()
    )
    
@router.message(Command('help'), ~StateFilter(FSMPracticing.stresses, FSMPracticing.prototypes))
async def process_help_command(message: Message):
    await message.answer(
        text=LEXICON_RU['/help'],
        reply_markup=get_menu_keyboard()
    )
    
@router.message(F.text.lower().in_(['/stats', '📊 статистика', 'статистика']), \
                ~StateFilter(FSMPracticing.stresses, FSMPracticing.prototypes))
async def process_stats_command(message: Message, state: FSMContext):
    if await state.get_state() not in (FSMPracticing.stresses, FSMPracticing.prototypes):
        await state.clear()
    
    await message.reply(text='Выберите раздел:',
                        reply_markup=get_statistics_keyboard())
    
@router.message(F.text.lower().in_(['/settings', '⚙️ настройки', 'настройки']), \
                ~StateFilter(FSMPracticing.stresses, FSMPracticing.prototypes))
async def process_settings_command(message: Message, state: FSMContext):
    if await state.get_state() not in (FSMPracticing.stresses, FSMPracticing.prototypes):
        await state.clear()
    
    await message.answer(text=LEXICON_RU['/settings'], 
                         reply_markup=get_settings_keyboard())

@router.message(Command('cancel'), StateFilter(FSMPracticing.in_choosing_practice, \
                FSMPracticing.in_choosing_prototypes))
async def process_cancel_choosing(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text='Главное меню',
                         reply_markup=get_menu_keyboard())

@router.message(Command('cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text=LEXICON_RU['impossible_cancel']
    )
    
@router.message(~F.data == 'stresses', StateFilter(FSMPracticing.in_choosing_practice))
async def process_not_stated_choosing(message: Message):
    await message.answer(
        text=LEXICON_RU['not_stated_practicing']
    )