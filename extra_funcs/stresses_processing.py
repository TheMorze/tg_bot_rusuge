import random
from lexicon.stresses import STRESSES

def choose_random_stress() -> str:
    word = random.choice(list(STRESSES.keys()))
    options = set(STRESSES[word][0])
    correct = STRESSES[word][1]
    return (word, options, correct)