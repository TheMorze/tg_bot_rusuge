from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


kb_builder = ReplyKeyboardBuilder()

# Кнопки для клавиатуры
buttons = [
    KeyboardButton(text='🥷 Практиковаться'),
    KeyboardButton(text='📊 Статистика'),
    KeyboardButton(text='🏆 Список лидеров')
]

kb_builder.add(buttons[0])
kb_builder.row(*buttons[1:], width=2)

menu_keyboard = kb_builder.as_markup(resize_keyboard=True)
