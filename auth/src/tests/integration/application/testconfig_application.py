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

        