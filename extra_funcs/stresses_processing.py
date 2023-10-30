from database.users import Users

def process_correct(user_id: int):
    user_score = Users.get_user_score(user_id=user_id) + 1
    user_correct =  Users.get_user_correct(user_id=user_id) + 1
    Users.set_user_score(user_id=user_id, user_score=user_score)
    Users.set_user_correct(user_id=user_id, user_correct=user_correct)
    
def process_not_correct(user_id: int):
    user_not_correct = Users.get_user_not_correct(user_id=user_id) + 1
    Users.set_user_not_correct(user_id=user_id, user_not_correct=user_not_correct)