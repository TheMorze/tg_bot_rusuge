import sqlite3
from typing import Tuple

class Prototype:
    __DATABASE = 'db.sqlite3'
    
    @classmethod
    def get_random_tasks(cls, prototype: int) -> Tuple[str, list[str], str]:
        with sqlite3.connect(cls.__DATABASE) as connection:
            cursor = connection.cursor()
            cursor.execute(f"""SELECT text, source, correct_answer
                            FROM prototypes_{prototype}
                            ORDER BY RANDOM()
                            LIMIT 3""")
            data = list(cursor.fetchall())
            
            return data
    