from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.lexicon import PROTOTYPES

def get_practice_list() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🎯 Ударения', callback_data='stresses')],
    ])
    
    return ikb

def get_solving_list() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=PROTOTYPES['prototype_9'], callback_data='prototype_9')],
        [InlineKeyboardButton(text=PROTOTYPES['prototype_10'], callback_data='prototype_10')]
    ])
    
    return ikb

def get_settings_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Сбросить статистику', callback_data='reset_stats')],
        [InlineKeyboardButton(text='FAQ', callback_data='FAQ')]
    ])
    
    return ikb

def get_statistics_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🎯 Ударения', callback_data='stresses_stats')],
        [InlineKeyboardButton(text=PROTOTYPES['prototype_9'], callback_data='prototype_stats_9')],
        [InlineKeyboardButton(text=PROTOTYPES['prototype_10'], callback_data='prototype_stats_10')]    
    ])
    
    return ikb

def get_portions() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='5', callback_data='portion_5')],
        [InlineKeyboardButton(text='10', callback_data='portion_10')],
        [InlineKeyboardButton(text='20', callback_data='portion_20')]
    ])
    
    return ikb

