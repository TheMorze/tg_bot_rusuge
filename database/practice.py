import sqlite3
from typing import Tuple

class Stresses:
    __DATABASE = 'db.sqlite3'
    
    @classmethod
    def get_random_words(cls) -> Tuple[str, list[str], str]:
        with sqlite3.connect(cls.__DATABASE) as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT word, options, correct_answer
                            FROM stresses
                            ORDER BY RANDOM()
                            LIMIT 20""")
            data = list(cursor.fetchall())
            
            return data