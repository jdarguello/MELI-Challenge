from src.application.usecases.cache_service import CacheService
from src.application.usecases.userService import UserService

# Objetivo: validar la integridad de las credenciales del usuario, contrastarlo con el cache y, si es necesario, con la bd relacional
class AuthManager:
    def __init__(self):
        self.cache_service = CacheService()
        self.user_service = UserService()

    def valid_credentials(self, username, token):
        result = False
        if len(username) > 4 and len(token) > 10:
            result = True
        return result

    def validate_user_against_cache(self, username, token):
        user = self.cache_service.get_user(username)
        if user is not None and user.token == token:
            return True
        return False

    def validate_token_date(self, user):
        if user is not None:
            return user.valid_token()
        return False

    def register_user_in_cache(self, user):
        self.cache_service.set_user(user.username, user)
        return True
    
    def register_user_in_db(self, username, token, identity_provider_id):
        return self.user_service.create(
            username=username,
            token=token,
            identity_provider_id=identity_provider_id
        )