from src.tests.testconfig import TestConfig
from src.application.usecases.type_service import TypeService
from sqlalchemy.orm.exc import NoResultFound

class TestTypeService(TestConfig):
    def setUp(self):
        super().setUp()
        self.typeService = TypeService()

        for kind in ["Create", "Read", "Update", "Delete"]:
            self.typeService.permissionService.create(kind)
        
        self.vp_type = {
            "name": "VP",
            "description": "Vicepresidente de Finanzas",
            "weight": 100
        }

    def test_create_and_get_type_with_permissions(self):
        full_stack = self.typeService.create("Read", name="Full-stack", description="Desarrollador full-stack", weight=100)
        self.assertIsNotNone(full_stack.typeId)

        full_stack_saved = self.typeService.get(full_stack.typeId)
        self.assertEqual(full_stack_saved.name, full_stack.name)
        self.assertEqual(full_stack_saved.permissions[0].kind, "Read")
    
    def test_create_type_with_iniexistent_permission(self):
        with self.assertRaises(NoResultFound) as error:
            self.typeService.create("NotExists", name="Full-stack", description="Desarrollador full-stack", weight=100)
        self.assertEqual(str(error.exception), "Permission 'NotExists' not found")
    
    def test_get_type_that_not_exists(self):
        self._not_found_type_error(-1, self.typeService.get)
    
    def test_update_type(self):
        vp = self.typeService.create("Read", **self.vp_type)
        vp_updated = self.typeService.update(vp.typeId, "Create", name="VP Finanzas", weight=1000)
        self.assertEqual(vp_updated.name, "VP Finanzas")
        self.assertEqual(len(vp_updated.permissions), 2)
        self.assertFalse(self.typeService.permission_exists(vp_updated,"Update"))
        self.assertTrue(self.typeService.permission_exists(vp_updated,"Create"))
        self.assertEqual(vp_updated.permissions[0].kind, "Create")
        self.assertEqual(vp_updated.permissions[1].kind, "Read")
    
    def test_delete_permission_that_exists(self):
        vp = self.typeService.create(**self.vp_type)
        self.assertIsNotNone(self.typeService.get(vp.typeId))
        self.typeService.delete(vp.typeId)
        self._not_found_type_error(vp.typeId, self.typeService.get)
    
    def test_delete_permission_that_not_exists(self):
        type_id = -1
        self._not_found_type_error(type_id, self.typeService.delete)
    

    def _not_found_type_error(self, type_id, func):
        with self.assertRaises(NoResultFound) as error:
            func(type_id)
        self.assertEqual(str(error.exception), "Type with typeId=" + str(type_id) + " not found")