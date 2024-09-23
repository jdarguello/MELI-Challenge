from src.application.usecases.authManager import AuthManager
from flask import request, jsonify

class AuthDecorators:
    def __init__(self):
        self.auth_manager = AuthManager()

    # Decorador para validar la autenticación
    def auth_required(self):
        def decorator(func):
            def wrapper(*args, **kwargs):
                # Obtención y validación de variables del Header
                username, token, identity_provider_id = self._header_variables(request.headers)
                message, status_code = self._validate_headers(username, token, identity_provider_id)
                if status_code != 200:
                    return jsonify(message), status_code
                # Ejecución de escenarios de validación
                self.auth_manager.auth_validation_flows(username, token, identity_provider_id)
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    
    def role_required(self, role):
        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    def _header_variables(self, headers):
        username, token, identity_provider_id = None, None, None
        if 'username' in headers:
            username = headers['username']
        if 'token' in headers:
            token = headers['token']
        if 'identity_provider_id' in headers:
            identity_provider_id = headers['identity_provider_id']
        return username, token, identity_provider_id
    
    def _validate_headers(self, username, token, identity_provider_id):
        for var in [("username", username), ("Authorization", token), ("identity_provider_id", identity_provider_id)]:
            if var[1] is None:
                return {"message": "Missing header: " + var[0]}, 400
        return {"message": "All OK"}, 200
    

    


