from src.tests.integration.application.testconfig_application import TestConfigApplication
from src.application.usecases.userService import UserService
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime

class TestUserService(TestConfigApplication):
    def setUp(self):
        super().setUp()
        self.userService = UserService()
        self.setup_user_test_info()

    def test_create_and_get_user_with_role_and_idp(self):
        john = self.userService.create(**self.users[0])
        john_db = self.userService.get_by_id(john.userId)
        self.assertEqual(john_db.username, self.users[0]["username"])
        self.assertEqual(john_db.token, self.users[0]["token"])
        self.assertEqual(john_db.identity_provider.identityProviderId, self.idps[0]["identityProviderId"])

        john = self.userService.assign_role(john.userId, self.roles[0]["roleId"])
        john_db = self.userService.get_by_id(john.userId)
        self.assertEqual(len(john_db.roles), 1)
        self.assertEqual(john_db.roles[0].roleId, self.roles[0]["roleId"])
    
    def test_get_non_existent_user(self):
        self._not_found_user_error(-1, self.userService.get_by_id)
    
    def test_get_users_by_idp(self):
        self.userService.create(**self.users[1])
        self.userService.create(**self.users[2])
        users = self.userService.get_all_by_idp(self.idps[1]["identityProviderId"])
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].username, self.users[1]["username"])
        self.assertEqual(users[1].username, self.users[2]["username"])
    
    def test_assign_and_remove_role_to_user(self):
        john = self.userService.create(**self.users[0])
        self.userService.assign_role(john.userId, self.roles[0]["roleId"])
        self.userService.assign_role(john.userId, self.roles[0]["roleId"])  # If assigned again, it should ignore it
        john = self.userService.get_by_id(john.userId)
        self.assertEqual(len(john.roles), 1)
        self.assertEqual(john.roles[0].roleId, self.roles[0]["roleId"])

        self.userService.remove_role(john.userId, self.roles[0]["roleId"])
        self.userService.remove_role(john.userId, self.roles[0]["roleId"]) # If removed again, it should ignore it and not raise an error
        self.assertEqual(len(john.roles), 0)

    def test_update_user(self):
        john = self.userService.create(**self.users[0])
        john = self.userService.update(john.userId, token="new1233")
        john_db = self.userService.get_by_id(john.userId)
        self.assertEqual(john_db.username, self.users[0]["username"])
        self.assertEqual(john_db.token, "new1233")
        
    def test_delete_user_that_exists(self):
        johan = self.userService.create(**self.users[1])
        self.assertIsNotNone(self.userService.get_by_id(johan.userId))
        self.userService.delete(johan.userId)
        self._not_found_user_error(johan.userId, self.userService.get_by_id)
    
    def test_delete_role_that_not_exists(self):
        user_id = -1
        self._not_found_user_error(user_id, self.userService.delete)
    
    def _not_found_user_error(self, user_id, func):
        with self.assertRaises(NoResultFound) as error:
            func(user_id)
        self.assertEqual(str(error.exception), "User with userId=" + str(user_id) + " not found")