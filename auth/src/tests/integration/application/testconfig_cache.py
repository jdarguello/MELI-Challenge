from src.tests.integration.application.testconfig_application import TestConfigApplication
from src.application.usecases.userService import UserService
from src.root import get_env_vars, cache

class TestConfigCache(TestConfigApplication):
    env = get_env_vars({"env": "tests", "type": "integration"})

    def setUp(self):
        super().setUp()
        # Cache de prueba (db = 0)
        self.cache = cache

        # Data de prueba para la base de datos SQL
        self.userService = UserService()
        self.setup_user_test_info()

        for user_info in self.users:
            user = self.userService.create(**user_info)
            user_info["userId"] = user.userId
            self.userService.assign_role(user.userId, self.roles[0]["roleId"])
            self.userService.assign_role(user.userId, self.roles[1]["roleId"])
    
    def tearDown(self):
        super().tearDown()
        self.cache.flushdb()    # Limpiar cache de prueba (db = 0)
