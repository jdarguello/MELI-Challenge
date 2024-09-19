from src.tests.testconfig import TestConfig
from src.application.usecases.scopeService import ScopeService
from sqlalchemy.orm.exc import NoResultFound

class TestPermissionService(TestConfig):
    def setUp(self):
        super().setUp()
        self.scopeService = ScopeService()

    def test_create_and_get_permissions(self):
        for scope_info in [
            {"name": "VP TI", "description": "Área encargada de la administración de los servicios de TI"},
            {"name": "VP Jurídica", "description": "Área encargada de la administración de los servicios legales"},
            {"name": "VP Finanzas", "description": "Área encargada de la administración de los servicios financieros"},
        ]:
            scope = self.scopeService.create(scope_info["name"], scope_info["description"])
            self.assertIsNotNone(scope.scopeId)
            self.assertEqual(scope.name, scope_info["name"])
            self.assertEqual(scope.description, self.scopeService.get(scope.scopeId).description)
       
    def test_get_scope_that_not_exists(self):
        self.assertIsNone(self.scopeService.get(-1))
    
    def test_update_scope(self):
        vp_finanzas = self.scopeService.create("VP Finanzas", "Área que administra los servicios financieros")

        vp_juridica = self.scopeService.update(vp_finanzas.scopeId, "VP Jurídica")
        self.assertEqual(vp_juridica.name, "VP Jurídica")
        self.assertEqual(vp_juridica.description, vp_finanzas.description)

        vp_juridica = self.scopeService.update(vp_juridica.scopeId, new_description="Área que administra los servicios legales")
        self.assertEqual(vp_juridica.name, "VP Jurídica")
        self.assertEqual(vp_juridica.description, "Área que administra los servicios legales")

    def test_delete_permission_that_exists(self):
        vp_ti = self.scopeService.create("VP TI", "Área encargada de la administración de los servicios de TI")
        self.assertIsNotNone(self.scopeService.get(vp_ti.scopeId))
        self.scopeService.delete(vp_ti.scopeId)
        self.assertIsNone(self.scopeService.get(vp_ti.scopeId))

    def test_delete_permission_that_not_exists(self):
        scopeId = -1
        with self.assertRaises(NoResultFound) as error:
            self.scopeService.delete(scopeId)
        self.assertEqual(str(error.exception), "Scope with scopeId=" + str(scopeId) + " not found")