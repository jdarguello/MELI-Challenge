from src.tests.integration.application.testconfig_application import TestConfigApplication
from src.application.usecases.role_service import RoleService
from sqlalchemy.orm.exc import NoResultFound

class TestRoleService(TestConfigApplication):
    def setUp(self):
        super().setUp()
        self.roleService = RoleService()

        self.roles = [
            {"name": "VP Colombia", "description": "Vice Presidento Corporativo - Filial Colombia", "typeId": self.types[0]["typeId"], "scopeId": self.scopes[0]["scopeId"]},
            {"name": "Full-stack", "description": "Desarrollador full-stack", "typeId": self.types[1]["typeId"], "scopeId": self.scopes[0]["scopeId"]},
            {"name": "VP Brasil", "description": "Vice Presidento Corporativo - Filial Brasil", "typeId": self.types[0]["typeId"], "scopeId": self.scopes[1]["scopeId"]},
            {"name": "Full-stack BR", "description": "Desarrollador full-stack", "typeId": self.types[1]["typeId"], "scopeId": self.scopes[1]["scopeId"]}
        ]

    def test_create_and_get_role_with_type_and_scope(self):
        vp_colombia = self.roleService.create(**self.roles[0])
        vp_colombia_db = self.roleService.get_by_id(vp_colombia.roleId)
        self.assertEqual(vp_colombia_db.name, "VP Colombia")
        self.assertEqual(vp_colombia_db.description, "Vice Presidento Corporativo - Filial Colombia")
        self.assertEqual(vp_colombia_db.type.typeId, self.types[0]["typeId"])
        self.assertEqual(vp_colombia_db.scope.scopeId, self.scopes[0]["scopeId"])

    def test_get_non_existent_role(self):
        self._not_found_role_error(-1, self.roleService.get_by_id)
    
    def test_get_role_by_scope(self):
        vp_colombia = self.roleService.create(**self.roles[0])
        vp_brasil = self.roleService.create(**self.roles[2])
        roles = self.roleService.get_by_scope(self.scopes[0]["scopeId"])
        self.assertEqual(len(roles), 1)
        self.assertEqual(roles[0].name, "VP Colombia")

        full_stack_br = self.roleService.create(**self.roles[3])
        roles = self.roleService.get_by_scope(self.scopes[1]["scopeId"])
        self.assertEqual(len(roles), 2)
        self.assertEqual(roles[0].name, "VP Brasil")
        self.assertEqual(roles[1].name, "Full-stack BR")
    
    def test_update_role(self):
        self.roles[0]["name"] = "VP Brasil"
        self.roles[0]["description"] = "Vice Presidente Corporativo - Filial Brasil"
        vp_colombia = self.roleService.create(**self.roles[0])
        vp_colombia_updated = self.roleService.update(vp_colombia.roleId, new_name="VP Colombia", new_description="Vice Presidente Corporativo - Filial Colombia")
        self.assertEqual(vp_colombia_updated.name, "VP Colombia")
        self.assertEqual(vp_colombia_updated.description, "Vice Presidente Corporativo - Filial Colombia")
    
    def test_delete_role_that_exists(self):
        full_stack_col = self.roleService.create(**self.roles[1])
        self.assertIsNotNone(self.roleService.get_by_id(full_stack_col.roleId))
        self.roleService.delete(full_stack_col.roleId)
        self._not_found_role_error(full_stack_col.roleId, self.roleService.get_by_id)

    def test_delete_role_that_not_exists(self):
        role_id = -1
        self._not_found_role_error(role_id, self.roleService.delete)
    

    def _not_found_role_error(self, role_id, func):
        with self.assertRaises(NoResultFound) as error:
            func(role_id)
        self.assertEqual(str(error.exception), "Role with roleId=" + str(role_id) + " not found")
    