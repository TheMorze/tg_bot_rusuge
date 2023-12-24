from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

class AnswerFromalization(BaseFilter):
    """Checks answer formalization"""
    
    def __init__(self, task_type: str):
        """
        Keyword args:
        
        task_type -- the type of task (example: 'prototypes')
        
        """
        
        self.digits_format = [9, 10]
        self.task_type = task_type
        
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        if self.task_type == 'prototypes':
            data = await state.get_data()
            prototype = data['prototype']
            if prototype in self.digits_format:
                answer = message.text
                return (
                    all(map(lambda x: x.isdigit(), answer))
                    and len(answer) < 10
                )