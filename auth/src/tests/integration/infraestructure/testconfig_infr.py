from src.tests.integration.application.testconfig_cache import TestConfigCache
from src.application.usecases.authManager import AuthManager
from src.root import app
from src.app import App
from unittest.mock import MagicMock, patch
import unittest
import json

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
        self.authManager = AuthManager()
    
    def mock_response(self, mock_get, url, json, status_code=200):
        # Define a mock response object with the attributes you need
        mock_response = MagicMock()
        mock_response.status_code = status_code
        mock_response.json = json
        mock_get.return_value = mock_response

        # Validar el request con los parámetros correctos
        #mock_get.assert_called_once_with(url, headers=headers)
    
    def mock_asserts(self, response, res_status_code, res_message, username, token):
        self.assertEqual(response.status_code, res_status_code)
        self.assertEqual(response.json, res_message)
        user_cache = self.authManager.cache_service.get_user(username)
        self.assertEqual(user_cache.token, token)
        self.assertEqual(user_cache.username, username)
        user_db = self.authManager.user_service.get_by_username(username)
        self.assertEqual(user_db.token, token)
    
    def get_request(self, url, json, headers):
        return self.client.get(url, json=json, headers=headers)