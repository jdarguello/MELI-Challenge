from src.application.usecases.authManager import AuthManager
from flask import request, jsonify
from functools import wraps

class AuthDecorators:
    def __init__(self):
        self.auth_manager = AuthManager()
        self.user_service = self.auth_manager.user_service

    # Decorador para validar la autenticación
    def auth_required(self):
        def decorator(func):
            @wraps(func)
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
    
    
    def role_required(self, role_weight):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Obtención y validación de variables del Header
                username, token, identity_provider_id = self._header_variables(request.headers)
                message, status_code = self._validate_headers(username, token, identity_provider_id)
                if status_code != 200:
                    return jsonify(message), status_code
                # Validación de roles
                user = self.user_service.get_by_username(username)
                if not self._is_superuser(user.roles) or self._max_weight(user.roles) < role_weight:  
                    return jsonify({"message": "Forbidden: you don't have a role with enough permissions."}), 403
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    def _is_superuser(self, roles):
        for role in roles:
            role_type = role.type
            if role_type.weight == 1000:
                return True
        return False
    
    def _max_weight(self, roles):
        max_value = 1
        for role in roles:
            role_type = role.type
            if role_type.weight > max_value:
                max_value = role_type.weight
        return max_value
    


    def apply_decorators(self, func, *decorators):
        for decorator in decorators:
            func = decorator(func)
        return func
    
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
    

    


