from src.tests.integration.application.testconfig_application import TestConfigApplication
from src.application.usecases.userService import UserService
from src.root import get_env_vars, cache

class TestConfigInfraestructure(TestConfigApplication):
    env = get_env_vars({"env": "tests", "type": "integration"})

    def setUp(self):
        super().setUp()
        # Cache de prueba (bd = 0)
        self.cache = cache
        self.cache.flushdb() # Limpia la base de datos de cache

        # Data de prueba para la db
        self.userService = UserService()
        self.setup_user_test_info()

