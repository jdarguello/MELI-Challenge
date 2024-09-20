from src.tests.testconfig import TestConfig
from src.application.usecases.permissionService import PermissionService
from sqlalchemy.orm.exc import NoResultFound

class TestPermissionService(TestConfig):
    def setUp(self):
        super().setUp()
        self.permissionService = PermissionService()

    def test_create_and_get_permissions(self):
        for kind_permission in ["Create", "Read", "Update", "Delete"]:
            permission = self.permissionService.create(kind_permission)
            self.assertIsNotNone(permission.permissionId)
            self.assertEqual(permission.kind, kind_permission)
            self.assertEqual(permission.kind, self.permissionService.get(kind_permission).kind)
        
    def test_get_permission_that_not_exists(self):
        kind_permission = "NotExists"
        self.get_permission_error(kind_permission)

    def test_update_permission(self):
        create_permission = self.permissionService.create("Create")

        list_permission = self.permissionService.update("Create", "List")
        self.assertEqual(create_permission.permissionId, list_permission.permissionId)
        self.assertEqual(list_permission.kind, "List")
    
    def test_delete_permission_that_exists(self):
        self.permissionService.create("Read")
        self.assertIsNotNone(self.permissionService.get("Read"))
        self.permissionService.delete("Read")
        self.get_permission_error("Read")

    def get_permission_error(self, kind_permission):
        with self.assertRaises(NoResultFound) as error:
            self.permissionService.get(kind_permission)
        self.assertEqual(str(error.exception), "Permission '" + kind_permission + "' not found")

    def test_delete_permission_that_not_exists(self):
        kind_permission = "NotExists"
        with self.assertRaises(NoResultFound) as error:
            self.permissionService.delete("NotExists")
        self.assertEqual(str(error.exception), "Permission '" + kind_permission + "' not found")
        