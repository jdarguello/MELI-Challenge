from src.tests.testconfig import TestConfig
from src.application.usecases.scopeService import ScopeService
from sqlalchemy.orm.exc import NoResultFound

class TestScopeService(TestConfig):
    def setUp(self):
        super().setUp()
        self.scopeService = ScopeService()

        self.vp_ti = {"name": "VP TI", "description": "Área encargada de la administración de los servicios de TI"}
        self.vp_juridica = {"name": "VP Jurídica", "description": "Área encargada de la administración de los servicios legales"}
        self.vp_finanzas = {"name": "VP Finanzas", "description": "Área encargada de la administración de los servicios financieros"}

    def test_create_and_get_permissions(self):
        for scope_info in [self.vp_ti, self.vp_juridica, self.vp_finanzas]:
            scope = self.scopeService.create(scope_info["name"], scope_info["description"])
            self.assertIsNotNone(scope.scopeId)
            self.assertEqual(scope.name, scope_info["name"])
            self.assertEqual(scope.description, self.scopeService.get(scope.scopeId).description)
       
    def test_get_scope_that_not_exists(self):
        self.assertIsNone(self.scopeService.get(-1))
    
    def test_update_scope(self):
        vp_finanzas = self.scopeService.create(self.vp_finanzas["name"], self.vp_finanzas["description"])

        vp_juridica = self.scopeService.update(vp_finanzas.scopeId, self.vp_juridica["name"])
        self.assertEqual(vp_juridica.name, self.vp_juridica["name"])
        self.assertEqual(vp_juridica.description, vp_finanzas.description)

        vp_juridica = self.scopeService.update(vp_juridica.scopeId, new_description=self.vp_juridica["description"])
        self.assertEqual(vp_juridica.name, self.vp_juridica["name"])
        self.assertEqual(vp_juridica.description, self.vp_juridica["description"])

    def test_delete_permission_that_exists(self):
        vp_ti = self.scopeService.create(self.vp_ti["name"], self.vp_ti["description"])
        self.assertIsNotNone(self.scopeService.get(vp_ti.scopeId))
        self.scopeService.delete(vp_ti.scopeId)
        self.assertIsNone(self.scopeService.get(vp_ti.scopeId))

    def test_delete_permission_that_not_exists(self):
        scope_id = -1
        with self.assertRaises(NoResultFound) as error:
            self.scopeService.delete(scope_id)
        self.assertEqual(str(error.exception), "Scope with scopeId=" + str(scope_id) + " not found")