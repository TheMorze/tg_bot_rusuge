import sqlite3, random

class Stresses:
    __DATABASE = 'db.sqlite3'
    
    @classmethod
    def get_random_word(cls) -> tuple[str, list[str], str]:
        with sqlite3.connect(cls.__DATABASE) as connection:
            cursor = connection.cursor()
            random_id = random.randint(1, 2) # Диапозон ID всех слов в БД
            cursor.execute("SELECT * FROM stresses WHERE id=?", (random_id,))
            data = list(cursor.fetchone())
            print(data)
            
            options = data[2].split(',')
            random.shuffle(options)
            data[2] = options
            
            return data[1:]