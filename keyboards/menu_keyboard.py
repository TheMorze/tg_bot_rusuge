from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_menu_keyboard() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()

    # Кнопки для клавиатуры меню
    buttons = [
        KeyboardButton(text='💡 Решать прототипы'),
        KeyboardButton(text='🥷 Практиковаться'),
        KeyboardButton(text='📊 Статистика'),
        KeyboardButton(text='⚙️ Настройки')
    ]

    kb_builder.row(*buttons[:2])
    kb_builder.row(*buttons[2:], width=2)

    menu_keyboard = kb_builder.as_markup(resize_keyboard=True)
    return menu_keyboard