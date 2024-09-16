from src.domain.entities.user import User

class UserService:
    def __init__(self, user: User):
        self.user = user

    def create_user(self, user_data):
        self.user.create_user(user_data)
    
    def get_user(self, user_id):
        return self.user.get_user(user_id)
    
    def get_users(self):
        return self.user.get_users()
    
    def update_user(self, user_id, user_data):
        return self.user.update_user(user_id, user_data)
    
    def delete_user(self, user_id):
        return self.user.delete_user(user_id)