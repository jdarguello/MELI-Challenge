from src.application.usecases.authManager import AuthManager
from src.infraestructure.adapters.outbound.oauth import OAuthProviderFlows 

class AuthAdapter:
    def __init__(self, app):
        self.app = app
        self.auth_manager = AuthManager()                   #Capa de persistencia
        self.oauth_provider_flows = OAuthProviderFlows()    #Servicios externos
        self.setup_routes()
    
    def setup_routes(self):
        self.app.route("/api/login")(self.login)

    def login(self):
        return "Hello, World!"

    