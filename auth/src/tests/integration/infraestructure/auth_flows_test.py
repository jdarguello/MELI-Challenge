from src.tests.integration.infraestructure.testconfig_infr import TestConfigInfraestructure
from src.application.usecases.authManager import AuthManager
from unittest.mock import MagicMock, patch
import unittest
import json

class TestAuthFlows(TestConfigInfraestructure):
    def setUp(self):
        super().setUp()
        self.authManager = AuthManager()

        # Almacena dos de los tres usuarios en caché
        self.john = self.authManager.user_service.get_by_username(self.users[0]['username'])
        self.johana = self.authManager.user_service.get_by_username(self.users[1]['username'])
        self.authManager.register_user_in_cache(self.john)

        # Json de prueba
        self.json = {
            'username': self.users[0]['username'],
            'token': self.users[0]["token"],
            'identity_provider_id': self.users[0]["identity_provider_id"]
        }

    def test_valid_creds(self):
        response = self.client.post('/api/validate-creds', json=self.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Credentials are valid"})
    
    def test_invalid_creds(self):
        response = self.client.post('/api/validate-creds', json={
            'username': 'user1',
            'token': '12',
            'identity_provider_id': '1'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Altered credentials"})

    @patch('src.infraestructure.adapters.outbound.oauth.requests.get')
    def test_invalid_user_in_cache_token_no_matched_Google_validation(self, mock_get):
        # Cambia el token de John para que entre en el flujo de validación de Google
        self.json['token'] = '123456789020393'
        # Define a mock response object with the attributes you need
        self.mock_response(self.john.username, mock_get)

        response = self.client.post('/api/validate-creds', json=self.json)

        # Validar el request con los parámetros correctos
        mock_get.assert_called_once_with(
            self.john.identity_provider.tokenValidationUrl,
            headers={'Authorization': f"Bearer {self.json['token']}"}
        )

        # Validar el token de John y su información en caché
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.json, {"message": "Token Updated"})
        user_cache = self.authManager.cache_service.get_user(self.john.username)
        self.assertEqual(user_cache.token, self.json['token'])
        self.assertEqual(user_cache.username, self.john.username)
        user_db = self.authManager.user_service.get_by_username(self.john.username)
        self.assertEqual(user_db.token, self.json['token'])
    
    @patch('src.infraestructure.adapters.outbound.oauth.requests.get')
    def test_new_user_Google_validation(self, mock_get):
        # Nuevo usuario: Johana. Sin registros en base de datos ni caché
        self.authManager.user_service.delete(self.johana.userId)

        self.mock_response(self.johana.username, mock_get)

        response = self.client.post('/api/validate-creds', json={
            'username': self.johana.username,
            'token': self.johana.token,
            'identity_provider_id': self.johana.identityProviderId
        })
        
        # Validar el request con los parámetros correctos
        mock_get.assert_called_once_with(
            self.johana.identity_provider.tokenValidationUrl,
            headers={'Authorization': f"Bearer {self.johana.token}"}
        )

        # Validar el token de Johana y su información en caché y en base de datos
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "User registered!"})
        user_cache = self.authManager.cache_service.get_user(self.johana.username)
        self.assertEqual(user_cache.token, self.johana.token)
        self.assertEqual(user_cache.username, self.johana.username)
        user_db = self.authManager.user_service.get_by_username(self.johana.username)
        self.assertEqual(user_db.token, self.johana.token)
        self.assertEqual(user_db.username, self.johana.username)
        self.assertEqual(user_db.identityProviderId, self.johana.identityProviderId)
    
    @patch('src.infraestructure.adapters.outbound.oauth.requests.get')
    def test_new_user_GitHub_validation(self, mock_get):
        # Nuevo usuario: Johana. Sin registros en base de datos ni caché
        self.authManager.user_service.delete(self.johana.userId)

        # Define a mock response object with the attributes you need
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json = {
            'login': self.johana.username,
            'id': "true",
            "nodid": "3568",
            "avatar_url": "https://www.github.com/auth/userinfo.email"
        }
        mock_get.return_value = mock_response

        response = self.client.post('/api/validate-creds', json={
            'username': self.johana.username,
            'token': self.johana.token,
            'identity_provider_id': self.johana.identityProviderId
        })
        
        # Validar el request con los parámetros correctos
        mock_get.assert_called_once_with(
            self.johana.identity_provider.tokenValidationUrl,
            headers={'Authorization': f"Bearer {self.johana.token}"}
        )

        # Validar el token de Johana y su información en caché y en base de datos
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "User registered!"})
        user_cache = self.authManager.cache_service.get_user(self.johana.username)
        self.assertEqual(user_cache.token, self.johana.token)
        self.assertEqual(user_cache.username, self.johana.username)
        user_db = self.authManager.user_service.get_by_username(self.johana.username)
        self.assertEqual(user_db.token, self.johana.token)
        self.assertEqual(user_db.username, self.johana.username)
        self.assertEqual(user_db.identityProviderId, self.johana.identityProviderId)


    @patch('src.infraestructure.adapters.outbound.oauth.requests.get')
    def test_existing_user_role_checks(self, mock_get):
        self.mock_response(self.johana.username, mock_get)

        response = self.client.get('/api/my-roles', json={}, headers={
                'token': self.johana.token,
                'username': self.johana.username,
                'identity_provider_id': self.johana.identityProviderId
            })
        
        # Validar el request con los parámetros correctos
        mock_get.assert_called_once_with(
            self.johana.identity_provider.tokenValidationUrl,
            headers={'Authorization': f"Bearer {self.johana.token}"})
        
        # Validar la respuesta
        self.assertEqual(response.status_code, 200)
        roles_dict = json.loads(json.dumps(response.json))
        self.assertEqual(roles_dict[0]["name"], self.johana.roles[0].name)
        self.assertEqual(roles_dict[0]["description"], self.johana.roles[0].description)
        self.assertEqual(roles_dict[1]["name"], self.johana.roles[1].name)
        self.assertEqual(roles_dict[1]["description"], self.johana.roles[1].description)

    def mock_response(self, username, mock_get):
        # Define a mock response object with the attributes you need
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json = {
            'email': username,
            'email_verified': "true",
            "expires_in": "3568",
            "scope": "openid https://www.googleapis.com/auth/userinfo.email"
        }
        mock_get.return_value = mock_response