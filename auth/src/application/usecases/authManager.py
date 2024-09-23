from src.application.usecases.cache_service import CacheService
from src.application.usecases.userService import UserService
from src.application.usecases.identity_provider_service import IdentityProviderService

# Objetivo: validar la integridad de las credenciales del usuario, contrastarlo con el cache y, si es necesario, con la bd relacional
class AuthManager:
    def __init__(self):
        self.cache_service = CacheService()
        self.user_service = UserService()
        self.identity_provider_service = IdentityProviderService()

    def valid_credentials(self, username, token):
        result = False
        if len(username) > 4 and len(token) > 10:
            result = True
        return result

    def validate_user_against_cache(self, username, token):
        user = self.cache_service.get_user(username)
        if user is not None and user.token == token:
            return (True, user)
        elif user is not None:
            return (False, user)
        return (False, None)

    def validate_token_date(self, user):
        if user is not None:
            return user.valid_token()
        return False
    
    def validate_idp_request(self, user, token, status_code, json, new_user=False):
        # Obtención del username
        idp_username = self.get_idp_username(json)
        if status_code == 200 and user.username == idp_username:
            #El token es válido, se registra el usuario en caché y en la bd
            user.token = token
            user = self.register_user_in_db(user.username, token, user.identityProviderId)
            self.register_user_in_cache(user)
            if new_user:
                return {"message": "User registered!"}, 201
            return {"message": "Token Updated"}, 202
        elif status_code == 200 and user.username != json['email']:
            #El token es válido, pero el usuario no coincide con el token
            return {"message": "Security Risk"}, 401
        return json, status_code
    
    def get_idp_username(self, json):
        if 'email' in json:
            return json['email']    #Google
        elif 'login' in json:
            return json['login']    #GitHub
        return None

    def register_user_in_cache(self, user):
        self.cache_service.set_user(user.username, user)
        return True
    
    def register_user_in_db(self, username, token, identity_provider_id):
        return self.user_service.update_or_create(
            username=username,
            token=token,
            identity_provider_id=identity_provider_id
        )