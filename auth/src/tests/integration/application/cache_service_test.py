from src.tests.integration.application.testconfig_cache import TestConfigCache
from src.application.usecases.cache_service import CacheService

class TestCacheService(TestConfigCache):
    def setUp(self):
        super().setUp()
        self.cacheService = CacheService()

        self.user_john_doe = self.cacheService.user_service.get_by_id(self.users[0]["userId"])
        self.user_susan = self.cacheService.user_service.get_by_id(self.users[2]["userId"])

    def test_user_cache_operations(self):
        self.cacheService.set_user(self.user_john_doe.username, self.user_john_doe)
        self.cacheService.set_user(self.user_susan.username, self.user_susan)

        user_cache = self.cacheService.get_user(self.user_john_doe.username)
        self.assertIsNotNone(user_cache)
        self.assertEqual(self.user_john_doe.username, user_cache.username)
        self.assertEqual(self.user_john_doe.token, user_cache.token)
        self.assertEqual(self.user_john_doe.tokenExpiryStart, user_cache.tokenExpiryStart)

        user_cache = self.cacheService.get_user(self.user_susan.username)
        self.assertIsNotNone(user_cache)
        self.assertEqual(self.user_susan.username, user_cache.username)
        self.assertEqual(self.user_susan.token, user_cache.token)
        self.assertEqual(self.user_susan.tokenExpiryStart, user_cache.tokenExpiryStart)
    
    def test_no_user_cache(self):
        self.assertIsNone(self.cacheService.get_user("john_doe_nonexistent"))
        self.assertIsNone(self.cacheService.get_user("susana_nonexistent"))