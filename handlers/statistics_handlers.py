from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.state import default_state
from aiogram.filters import StateFilter

from lexicon.lexicon import LEXICON_RU, PROTOTYPES
from database.user_stats import UserStats

router: Router = Router()

@router.callback_query(F.data == 'stresses_stats')
async def process_stresses_stats(callback: CallbackQuery):
    user_id = callback.from_user.id

    correct = UserStats.get_user_correct(user_id=user_id,
                                         topic_name='stresses')
    incorrect = UserStats.get_user_incorrect(user_id=user_id,
                                             topic_name='stresses')
    
    await callback.message.edit_text(text=LEXICON_RU['display_stats'].format(
                                    topic='🎯 Ударения', 
                                    correct=correct,
                                    incorrect=incorrect))
    await callback.answer()
    
@router.callback_query(F.data.startswith('prototype_stats'))
async def process_prototypes_stats(callback: CallbackQuery):
    user_id = callback.from_user.id

    prototype = callback.data.split('_')
    prototype = f'{prototype[0]}_{prototype[2]}'
    print(prototype)

    correct = UserStats.get_user_correct(user_id=user_id,
                                         topic_name=prototype)
    incorrect = UserStats.get_user_incorrect(user_id=user_id,
                                             topic_name=prototype)
    
    await callback.message.edit_text(text=LEXICON_RU['display_stats'].format(
                                    topic=PROTOTYPES[prototype],
                                    correct=correct,
                                    incorrect=incorrect)
                                )
    await callback.answer()