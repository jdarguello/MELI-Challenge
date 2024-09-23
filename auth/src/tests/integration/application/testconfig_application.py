from src.tests.testconfig import TestConfig
from src.application.usecases.type_service import TypeService
from src.application.usecases.scopeService import ScopeService
from src.application.usecases.permissionService import PermissionService

class TestConfigApplication(TestConfig):
    def setUp(self):
        super().setUp()

        self.setup_permissions()
        self.setup_types()
        self.setup_scopes()

        self.roles = [
            {"name": "VP Colombia", "description": "Vice Presidento Corporativo - Filial Colombia", "type_id": self.types[0]["typeId"], "scope_id": self.scopes[0]["scopeId"]},
            {"name": "Full-stack", "description": "Desarrollador full-stack", "type_id": self.types[1]["typeId"], "scope_id": self.scopes[0]["scopeId"]},
            {"name": "VP Brasil", "description": "Vice Presidento Corporativo - Filial Brasil", "type_id": self.types[0]["typeId"], "scope_id": self.scopes[1]["scopeId"]},
            {"name": "Full-stack BR", "description": "Desarrollador full-stack", "type_id": self.types[1]["typeId"], "scope_id": self.scopes[1]["scopeId"]}
        ]
    
    def setup_user_test_info(self):
        # Roles
        for role_info in self.roles:
            role = self.userService.role_service.create(**role_info)
            role_info["roleId"] = role.roleId
        
        # Identity Providers
        self.idps = [
            {"clientId": "10394", "name": "Google", "clientSecret": "1j3n", "tokenValidationUrl": "https://www.google.com", "tokenExpiryTime": 3600},
            {"clientId": "10395", "name": "Facebook", "clientSecret": "1j3n", "tokenValidationUrl": "https://www.facebook.com", "tokenExpiryTime": 900},
            {"clientId": "10396", "name": "Twitter", "clientSecret": "1j3n", "tokenValidationUrl": "https://www.twitter.com", "tokenExpiryTime": 1800}
        ]
        for idp_info in self.idps:
            idp = self.userService.identity_provider_service.create(**idp_info)
            idp_info["identityProviderId"] = idp.identityProviderId

        # Usuarios
        self.users = [
            {"username": "jon_doe@example.com", "token": "2234eu3n2j23", "identity_provider_id": self.idps[0]["identityProviderId"]},
            {"username": "johana@example.com", "token": "2jn33h3h33j3j", "identity_provider_id": self.idps[1]["identityProviderId"]},
            {"username": "susan@example.com", "token": "2jn33h3h33j3j",  "identity_provider_id": self.idps[1]["identityProviderId"]},
            {"username": "juanda@example.com", "token": "2234eu3n2j23", "identity_provider_id": self.idps[0]["identityProviderId"]}
        ]
        

    def setup_permissions(self):
        permission_service = PermissionService()
        for kind in ["Create", "Read", "Update", "Delete"]:
            permission_service.create(kind)

    def setup_types(self):
        type_service = TypeService()
        self.types = [
            {
                "name": "VP",
                "description": "Vicepresidente Corporativo",
                "weight": 1000,
                "permissions": ["Read", "Create"]
            },
            {
                "name": "Full-stack",
                "description": "Desarrollador full-stack",
                "weight": 100,
                "permissions": ["Read"]
            }
        ]

        for type_info in self.types:
            permissions = type_info["permissions"]
            type_info.pop("permissions")
            type_obj = type_service.create(*permissions, **type_info)
            type_info["typeId"] = type_obj.typeId
    
    def setup_scopes(self):
        scope_service = ScopeService()
        self.scopes = [
            {
                "name": "Filial Colombia",
                "description": "Estructura MeLi Colombia"
            },
            {
                "name": "Filial Brasil",
                "description": "Estructura MeLi Brasil"
            }
        ]

        for scope_info in self.scopes:
            scope_obj = scope_service.create(**scope_info)
            scope_info["scopeId"] = scope_obj.scopeId

        