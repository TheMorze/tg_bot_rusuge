from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, \
                                   ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon import LEXICON_RU

# Инициализация роутера уровня модуля
router = Router()

kb_builder = ReplyKeyboardBuilder()

# Кнопки для клавиатуры
buttons = [
    KeyboardButton(text='🎯 Ударения')
]

kb_builder.row(*buttons, width=2)

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text=LEXICON_RU['/start'],
        reply_markup=kb_builder.as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
    )
    
@router.message(Command('help'))
async def process_help_command(message: Message):
    await message.answer(
        text=LEXICON_RU['/help'],
        reply_markup=kb_builder.as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
    )