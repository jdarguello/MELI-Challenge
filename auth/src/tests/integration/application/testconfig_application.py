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

        