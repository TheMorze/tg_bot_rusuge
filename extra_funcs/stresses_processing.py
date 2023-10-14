import random
from lexicon.stresses import STRESSES

def choose_random_stress() -> str:
    word = random.choice(list(STRESSES.keys()))
    options = set(STRESSES[word])
    return (word, options)