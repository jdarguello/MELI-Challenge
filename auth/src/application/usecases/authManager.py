from src.application.usecases.userService import UserService
from src.application.usecases.cache_service import CacheService

# Objetivo: validar la integridad de las credenciales del usuario, contrastarlo con el cache y, si es necesario, con la bd relacional
class AuthManager:
    def __init__(self):
        self.userService = UserService()
        self.cacheService = CacheService()

    def valid_credentials(self, username, token):
        