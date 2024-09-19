from src.tests.integration.domain.testconfig_domain import TestConfigDomain
from src.domain.entities.role import Role

# Objetivo: Ejecutar operaciones CRUD contra la base de datos de prueba
class TestRoleTypeScope(TestConfigDomain):
    def test_create_type_enroll_one_permission(self):
        # Crea una instancia de Role, la relaciona con el scope Corporate, el Type Admin y la almacena en la BD
        vp_marketing = Role(name='VP Marketing', description='Vicepresidente de mercadeo')
        vp_marketing.type = self.admin
        vp_marketing.scope = self.corporate
        self.db.session.add(vp_marketing)
        self.db.session.commit()

        # Verifica que la instancia se haya guardado correctamente
        saved_role = self.db.session.get(Role, vp_marketing.roleId)
        self.assertEqual(saved_role.name, vp_marketing.name)
        self.assertEqual(saved_role.description, vp_marketing.description)
        self.assertEqual(saved_role.type.name, self.admin.name)
        self.assertEqual(saved_role.scope.name, self.corporate.name)

        #Además, verifica que el Role tenga permiso de Create
        self.assertEqual(len(saved_role.type.permissions), 1)
        self.assertEqual(saved_role.type.permissions[0].kind, self.create_permission.kind)