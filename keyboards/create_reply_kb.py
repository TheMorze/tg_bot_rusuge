from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon import LEXICON_RU

def create_reply_keyboard(width: int,
                          resize_keyboard: bool,
                          args: set[str]) -> ReplyKeyboardMarkup:
    
    # Инициализация билдера
    kb_builder = ReplyKeyboardBuilder()
    buttons: list[KeyboardButton] = []
    
    # Заполняем список кнопками из аргументов args
    if args:
        for button in args:
            buttons.append(KeyboardButton(
                text=button
            ))

    # Распаковка списка с кнопками в билдер с параметром width
    kb_builder.row(*buttons, width=width)
    
    # Возвращаем объект клавиатуры
    return kb_builder.as_markup(resize_keyboard=resize_keyboard)