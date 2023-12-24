from database.user_stats import UserStats

async def update_correct(user_id: int, topic_name: str, correct: int) -> None:
    user_correct = UserStats.get_user_correct(user_id=user_id,
                                              topic_name=topic_name) + correct
    UserStats.set_user_correct(user_id=user_id,
                               topic_name=topic_name,
                               user_correct=user_correct)
    
async def update_incorrect(user_id: int, topic_name: str, incorrect: int) -> None:
    user_incorrect = UserStats.get_user_incorrect(user_id=user_id,
                                                  topic_name=topic_name) + incorrect
    UserStats.set_user_incorrect(user_id=user_id,
                                 user_incorrect=user_incorrect,
                                 topic_name=topic_name)
    
async def update_stats(topic_name: str,
                       user_id: int,
                       user_correct: int,
                       user_incorrect: int):
    
    await update_correct(user_id=user_id,
                   topic_name=topic_name,
                   correct=user_correct)
    
    await update_incorrect(user_id=user_id,
                     topic_name=topic_name,
                     incorrect=user_incorrect)