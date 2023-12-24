from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.state import default_state
from aiogram.filters import StateFilter

from database.user_stats import UserStats

router: Router = Router()

@router.callback_query(F.data == 'reset_stats', StateFilter(default_state))
async def process_reset_stat(callback: CallbackQuery):
    UserStats.reset_stats(callback.from_user.id)
    
    await callback.answer(text='Статистика успешно сброшена!')
    
@router.callback_query(F.data == 'FAQ', StateFilter(default_state))
async def process_faq(callback: CallbackQuery):
    await callback.answer(text='you')