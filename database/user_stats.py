import sqlite3

class UserStats:
    __DATABASE = 'db.sqlite3'
            
    @classmethod
    def set_user_stats(cls, user_id):
        with sqlite3.connect(cls.__DATABASE) as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM user_stats
                           WHERE user_id=?""", 
                           (user_id,))
            
            current_id = cursor.fetchone()
            if not current_id:
                cursor.execute("""INSERT INTO 
                                    user_stats (user_id, topic_id)
                                VALUES
                                    (?, 1)""",
                                (user_id,))
    
    @classmethod
    def get_user_correct(cls, user_id: int, topic_name: str):
        with sqlite3.connect(cls.__DATABASE) as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT user_stats.correct 
                           FROM user_stats JOIN topics
                           ON user_stats.topic_id = topics.topic_id
                           WHERE user_stats.user_id=? AND topics.topic_name=?""", 
                           (user_id, topic_name))
            user_correct = cursor.fetchone()
            return user_correct[0]
    
    @classmethod
    def set_user_correct(cls, user_id: int, topic_name: str, user_correct: int):
        with sqlite3.connect(cls.__DATABASE) as connection:
            cursor = connection.cursor()
            cursor.execute("""UPDATE user_stats
                           SET correct=?
                           WHERE user_id=? AND topic_id=(
                                SELECT topic_id
                                FROM topics
                                WHERE topic_name=?)""", 
                           (user_correct, user_id, topic_name))
            
    @classmethod
    def get_user_incorrect(cls, user_id: int, topic_name: str):
        with sqlite3.connect(cls.__DATABASE) as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT user_stats.incorrect 
                           FROM user_stats JOIN topics
                           ON user_stats.topic_id = topics.topic_id
                           WHERE user_stats.user_id=? AND topics.topic_name=?""", 
                           (user_id, topic_name))
            user_incorrect = cursor.fetchone()
            return user_incorrect[0]
    
    @classmethod
    def set_user_incorrect(cls, user_id: int, topic_name: str, user_incorrect: int):
        with sqlite3.connect(cls.__DATABASE) as connection:
            cursor = connection.cursor()
            cursor.execute("""UPDATE user_stats
                           SET incorrect=?
                           WHERE user_id=? AND topic_id=(
                                SELECT topic_id
                                FROM topics
                                WHERE topic_name=?)""", 
                           (user_incorrect, user_id, topic_name))
    
    @classmethod
    def reset_stats(cls, user_id: int):
        with sqlite3.connect(cls.__DATABASE) as connection:
            cursor = connection.cursor()
            cursor.execute("""UPDATE user_stats
                           SET correct=0, incorrect=0
                           WHERE user_id=?""", (user_id,))
            
    