from src.tests.integration.application.testconfig_cache import TestConfigCache
from src.application.usecases.authManager import AuthManager
from src.root import app
from src.app import App

class TestConfigInfraestructure(TestConfigCache):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        App()   # Inicializar las rutas de la aplicación

    def setUp(self):
        super().setUp()
        self.app = app
        self.app.testing = True
        self.client = app.test_client()