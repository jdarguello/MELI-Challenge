from src.tests.integration.application.testconfig_cache import TestConfigCache
from src.application.usecases.authManager import AuthManager

class TestAuthManager(TestConfigCache):
    def setUp(self):
        super().setUp()
        self.authManager = AuthManager()

        #Users
        self.john = self.authManager.user_service.get_by_id(self.users[0]["userId"])
        self.susan = self.authManager.user_service.get_by_id(self.users[2]["userId"])

        #Cache
        self.authManager.cache_service.set_user(self.john.username, self.john)

    def test_valid_credentials(self):
        self.assertFalse(self.authManager.valid_credentials(".", "123j34h4h4j23"))
        self.assertFalse(self.authManager.valid_credentials("john_doe", "12"))
        self.assertTrue(self.authManager.valid_credentials(self.john.username, self.john.token))

    def test_validate_user_against_cache(self):
        self.assertFalse(self.authManager.validate_user_against_cache(self.susan.username, self.susan.token))
        self.assertTrue(self.authManager.validate_user_against_cache(self.john.username, self.john.token))
        self.assertFalse(self.authManager.validate_user_against_cache(self.john.username, "12jen3j34"))
    
    def test_register_user_in_cache(self):
        self.assertFalse(self.authManager.cache_service.get_user(self.susan.username))
        self.assertTrue(self.authManager.register_user_in_cache(self.susan))
        susan = self.authManager.cache_service.get_user(self.susan.username)
        self.assertEqual(susan.username, self.susan.username)
        self.assertEqual(susan.token, self.susan.token)
    
    def test_register_user_in_db(self):
        johana_user = self.authManager.register_user_in_db(
            self.users[1]["username"],
            self.users[1]["token"],
            self.users[1]["identity_provider_id"]
        )
        self.assertEqual(johana_user.username, self.users[1]["username"])
        self.assertEqual(johana_user.token, self.users[1]["token"])
        self.assertEqual(johana_user.identityProviderId, self.users[1]["identity_provider_id"])
