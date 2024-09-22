from src.tests.integration.domain.testconfig_domain import TestConfigDomain
from src.domain.entities.role import Role

# Objetivo: Ejecutar operaciones CRUD contra la base de datos de prueba
class TestRoleTypeScope(TestConfigDomain):
    def setUp(self):
        super().setUp()
        self.vp_marketing = Role(name='VP Marketing', description='Vicepresidente de mercadeo')
        self.vp_marketing.type = self.admin
        self.vp_marketing.scope = self.corporate

    def test_create_type_enroll_one_permission(self):
        # Crea una instancia de Role, la relaciona con el scope Corporate, el Type Admin y la almacena en la BD
        self.db.session.add(self.vp_marketing)
        self.db.session.commit()

        # Verifica que la instancia se haya guardado correctamente
        saved_role = self.db.session.get(Role, self.vp_marketing.roleId)
        self.assertEqual(saved_role.name, self.vp_marketing.name)
        self.assertEqual(saved_role.description, self.vp_marketing.description)
        self.assertEqual(saved_role.type.name, self.admin.name)
        self.assertEqual(saved_role.scope.name, self.corporate.name)

        #Además, verifica que el Role tenga permiso de Create
        self.assertEqual(len(saved_role.type.permissions), 1)
        self.assertEqual(saved_role.type.permissions[0].kind, self.create_permission.kind)
    
    def test_serialize_and_deseialize(self):
        self.db.session.add(self.vp_marketing)
        self.db.session.commit()

        # Verifica que la instancia se haya guardado correctamente
        saved_role = self.db.session.get(Role, self.vp_marketing.roleId)
        saved_role_serialized = saved_role.to_dict()
        self.assertEqual(saved_role_serialized['name'], self.vp_marketing.name)
        self.assertEqual(saved_role_serialized['description'], self.vp_marketing.description)
        self.assertEqual(saved_role_serialized['type']['name'], self.admin.name)
        self.assertEqual(saved_role_serialized['scope']['name'], self.corporate.name)
        self.assertEqual(saved_role_serialized['type']['permissions'][0]['kind'], self.create_permission.kind)

        # Verifica que la instancia se pueda reconstruir a partir de su representación serializada
        role = Role.from_dict(saved_role_serialized)
        self.assertEqual(role.name, self.vp_marketing.name)
        self.assertEqual(role.description, self.vp_marketing.description)
        self.assertEqual(role.type.name, self.admin.name)
        self.assertEqual(role.scope.name, self.corporate.name)
        self.assertEqual(role.type.permissions[0].kind, self.create_permission.kind)