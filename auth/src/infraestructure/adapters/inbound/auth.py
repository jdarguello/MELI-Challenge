from src.application.usecases.authDecorators import AuthDecorators
from flask import request, jsonify
import json

class AuthAdapter:
    def __init__(self, app):
        self.app = app
        self.auth_decorators = AuthDecorators()             #Decoradores
        self.auth_manager = self.auth_decorators.auth_manager
        self.setup_routes()
    
    def setup_routes(self):
        self.app.route("/api/validate-creds", methods=["POST"])(self.validate_creds)
        self.app.route("/api/my-roles", methods=["GET"])(self._apply_decorators(self.my_roles, self.auth_decorators.auth_required()))

    def validate_creds(self):
        username, token, identity_provider_id = self._get_vars(request.json)
        return self.auth_manager.auth_validation_flows(username, token, identity_provider_id)
    
    def my_roles(self):
        username, token, identity_provider_id = self.auth_decorators._header_variables(request.headers)
        message, status_code = self.auth_decorators._validate_headers(username, token, identity_provider_id)
        if status_code != 200:
            return jsonify(message), status_code
        roles = self.auth_manager.user_service.get_roles(username)
        return jsonify([role.to_dict() for role in roles]), 200
    
    def _get_vars (self, body):
        return body["username"], body["token"], body["identity_provider_id"]
    
    def _apply_decorators(self, func, *decorators):
        for decorator in decorators:
            func = decorator(func)
        return func

    