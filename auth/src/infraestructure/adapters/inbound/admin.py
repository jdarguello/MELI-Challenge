from src.application.usecases.authDecorators import AuthDecorators
from flask import request, jsonify, Blueprint
from src.root import app
import json

admin_bp = Blueprint('admin_bp', __name__)

# Operaciones de Súper Usuario
class AdminAdapter:
    def __init__(self):
        self.app = app
        self.auth_decorators = AuthDecorators()
        self.auth_manager = self.auth_decorators.auth_manager
        self.identity_provider_service = self.auth_manager.identity_provider_service
        self.setup_routes()
    
    def setup_routes(self):
        self.app.route("/api/admin/idp", methods=["POST", "PUT"])(self.auth_decorators.apply_decorators(self.admin_idp, 
            self.auth_decorators.auth_required(), self.auth_decorators.role_required(1000)))
        self.app.route("/api/admin/routes", methods=["GET"])(self.auth_decorators.apply_decorators(self.list_routes,
            self.auth_decorators.auth_required(), self.auth_decorators.role_required(1000)))

    def admin_idp(self):
        return self.identity_provider_service.register_idp_in_db(request.json, request.method)
    
    def list_routes(self):
        routes = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint == 'list_routes':
                continue
            
            route_info = {
                "endpoint": rule.endpoint,
                "methods": list(rule.methods),
                "route": str(rule)
            }
            routes.append(route_info)
        routes.sort(key=lambda x: x["endpoint"])
        
        return jsonify(routes)

admin_adapter = AdminAdapter()
    