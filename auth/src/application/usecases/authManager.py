from src.application.usecases.userService import UserService

class AuthManager:
    def __init__(self):
        self.userService = UserService()

    def login(self, email: str, token: str):
        user = self.userService.get_user_by_email(email)
        if user is None:
            return None
        if user.password != password:
            return None
        return user