from src.application.usecases.authManager import AuthManager
from src.infraestructure.adapters.outbound.oauth import OAuthProviderFlows 
from flask import request, jsonify

class AuthAdapter:
    def __init__(self, app):
        self.app = app
        self.auth_manager = AuthManager()                   #Capa de persistencia
        self.oauth_provider_flows = OAuthProviderFlows()    #Servicios externos
        self.setup_routes()
    
    def setup_routes(self):
        self.app.route("/api/validate-creds", methods=["POST"])(self.validate_creds)

    def validate_creds(self):
        username, token, identity_provider_id = self._get_vars(request.json)
        valid_creds = self.auth_manager.valid_credentials(username,token)
        valid_user, user = self.auth_manager.validate_user_against_cache(username,token)
        valid_token_date = self.auth_manager.validate_token_date(user)
        return self._validation_flows(username, user, token, identity_provider_id, valid_creds, valid_user, valid_token_date)
    
    def _get_vars (self, body):
        return body["username"], body["token"], body["identity_provider_id"]

    def _validation_flows(self, username, user, token, identity_provider_id, valid_creds, valid_user, valid_token_date):
        if valid_creds and valid_user and valid_token_date:
            return {"message": "Credentials are valid"}, 200
        elif not valid_creds:
            return {"message": "Altered credentials"}, 400
        elif not valid_user:
            #El usuario no se encontró en el caché. Es probable que sea un nuevo usuario
            json, status_code = self._oauth_verification_flow(username, user, token, identity_provider_id)
            return json, status_code
        elif not valid_token_date:
            return {"message": "Expired token"}, 401
        return {"message": "Invalid token"}, 401
    
    def _oauth_verification_flow(self, username, user, token, identity_provider_id):
        # Se valida el token con el proveedor de identidad
        new_user = False
        if user is not None:
            tokenValidationUrl = user.identity_provider.tokenValidationUrl
        else:
            new_user = True
            user = self.auth_manager.user_service.temporal_user(username, token, identity_provider_id)
            tokenValidationUrl = self.auth_manager.identity_provider_service.get_by_id(identity_provider_id).tokenValidationUrl
        status_code, json = self.oauth_provider_flows.token_validation(token, tokenValidationUrl)
        # Se evalúa la respuesta del proveedor de identidad
        json, status_code = self.auth_manager.validate_idp_request(user, token, status_code, json, new_user)
        return json, status_code

    