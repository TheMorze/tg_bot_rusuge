import sqlite3

class Database:
    __DATABASE = 'db.sqlite3'
    
    @classmethod
    def create_tables(cls):
        with sqlite3.connect(cls.__DATABASE) as connection:
            cursor = connection.cursor()
            
            cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY UNIQUE NOT NULL, 
                        user_name TEXT NOT NULL UNIQUE
                        )""")
            
            cursor.execute("""CREATE TABLE IF NOT EXISTS stresses (
                           id INTEGER PRIMARY KEY UNIQUE NOT NULL,
                           word TEXT(15) NOT NULL UNIQUE,
                           options TEXT(40) NOT NULL,
                           correct_answer TEXT(15) NOT NULL
                           )
                           """)
            
            cursor.execute("""CREATE TABLE IF NOT EXISTS user_stats (
                           user_id INTEGER NOT NULL REFERENCES users (id),
                           topic_id INTEGER NOT NULL REFERENCES topics (id),
                           correct INTEGER DEFAULT 0,
                           incorrect INTEGER DEFAULT 0
                           )
                           """)
            
            cursor.execute("""CREATE TABLE IF NOT EXISTS topics (
                           topic_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                           topic_name TEXT(20) UNIQUE NOT NULL
                           )
                           """)