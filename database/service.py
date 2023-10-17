import sqlite3

class Database:
    __DATABASE = 'C:\\Users\\kront\\OneDrive\\Рабочий стол\\bot_rus\\tg_bot_rusuge\\database\\db.sqlite3'
    
    @classmethod
    def create_users_table(cls):
        connection = sqlite3.connect(cls.__DATABASE)
        cursor = connection.cursor()
        print('СЕЙЧАС СОЗДАМ ТАБЛИЦУ')
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY NOT NULL, 
                    user_id INTEGER NOT NULL UNIQUE, 
                    user_name TEXT NOT NULL UNIQUE,
                    user_score INT DEFAULT 0,
                    user_correct INT DEFAULT 0,
                    user_not_correct INT DEFAULT 0
                )''')
        print('СОЗДАЛ ТАБЛИЦУ')
        connection.commit()
        connection.close()
        
    @classmethod
    def set_user(cls, user_id: int, user_name: str):
        connection = sqlite3.connect(cls.__DATABASE)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
        
        current_id = cursor.fetchone()
        print(current_id)
        if not current_id:
            cursor.execute('INSERT INTO users (user_id, user_name) VALUES (?, ?) ', (user_id, user_name))
            print('Добавил')
        connection.commit()
        connection.close()
    
    @classmethod
    def get_user_score(cls, user_id: int):
        connection = sqlite3.connect(cls.__DATABASE)
        cursor = connection.cursor()
        cursor.execute('SELECT user_score FROM users WHERE user_id=?', (user_id,))
        user_score = cursor.fetchone()
        connection.commit()
        connection.close()
        return user_score[0]
    
    @classmethod
    def set_user_score(cls, user_id: int, user_score: int):
        connection = sqlite3.connect(cls.__DATABASE)
        cursor = connection.cursor()
        cursor.execute('UPDATE users SET user_score=? WHERE user_id=?', (user_score, user_id))
        connection.commit()
        connection.close()
    
    @classmethod
    def get_user_correct(cls, user_id: int):
        connection = sqlite3.connect(cls.__DATABASE)
        cursor = connection.cursor()
        cursor.execute('SELECT user_correct FROM users WHERE user_id=?', (user_id,))
        user_correct = cursor.fetchone()
        connection.commit()
        connection.close()
        return user_correct[0]

    @classmethod
    def set_user_correct(cls, user_id: int, user_correct: int):
        connection = sqlite3.connect(cls.__DATABASE)
        cursor = connection.cursor()
        cursor.execute('UPDATE users SET user_correct=? WHERE user_id=?', (user_correct, user_id))
        connection.commit()
        connection.close()
        
    @classmethod
    def get_user_not_correct(cls, user_id: int):
        connection = sqlite3.connect(cls.__DATABASE)
        cursor = connection.cursor()
        cursor.execute('SELECT user_not_correct FROM users WHERE user_id=?', (user_id,))
        user_not_correct = cursor.fetchone()
        connection.commit()
        connection.close()
        return user_not_correct[0]
    
    @classmethod
    def set_user_not_correct(cls, user_id: int, user_not_correct: int):
        connection = sqlite3.connect(cls.__DATABASE)
        cursor = connection.cursor()
        cursor.execute('UPDATE users SET user_not_correct=? WHERE user_id=?', (user_not_correct, user_id))
        connection.commit()
        connection.close()