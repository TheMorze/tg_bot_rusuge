import sqlite3

class Users:
    __DATABASE = 'db.sqlite3'
    
    @classmethod
    def set_user(cls, user_id: int, user_name: str):
        with sqlite3.connect(cls.__DATABASE) as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM users 
                           WHERE user_id=?""", 
                           (user_id,))
            
            current_id = cursor.fetchone()
            if not current_id:
                cursor.execute("""INSERT INTO users (user_id, user_name) 
                               VALUES (?, ?)""", 
                               (user_id, user_name))