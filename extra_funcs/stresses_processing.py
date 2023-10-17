import random
from lexicon.stresses import STRESSES

from database.service import Database

def choose_random_stress() -> str:
    word = random.choice(list(STRESSES.keys()))
    options = set(STRESSES[word][0])
    correct = STRESSES[word][1]
    return (word, options, correct)

def process_correct(user_id: int):
    user_score = Database.get_user_score(user_id=user_id) + 1
    user_correct =  Database.get_user_correct(user_id=user_id) + 1
    Database.set_user_score(user_id=user_id, user_score=user_score)
    Database.set_user_correct(user_id=user_id, user_correct=user_correct)
    
def process_not_correct(user_id: int):
    user_not_correct = Database.get_user_not_correct(user_id=user_id) + 1
    Database.set_user_not_correct(user_id=user_id, user_not_correct=user_not_correct)