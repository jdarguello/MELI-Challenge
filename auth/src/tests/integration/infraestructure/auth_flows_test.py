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
        json = {
            'email': self.john.username,
            'email_verified': "true",
            "expires_in": "3568",
            "avatar_url": "https://www.google.com/auth/userinfo.email"
        }
        headers = {'Authorization': f"Bearer {self.json['token']}"}
        self.mock_response(mock_get, self.john.identity_provider.tokenValidationUrl,
            json)

        response = self.client.post('/api/validate-creds', json=self.json)

        # Validar el request con los parámetros correctos
        mock_get.assert_called_once_with(
            self.john.identity_provider.tokenValidationUrl,
            headers=headers)

        # Validar el token de John y su información en caché
        self.mock_asserts(response, 202, {"message": "Token Updated"}, self.john.username, self.json['token'])

    @patch('src.infraestructure.adapters.outbound.oauth.requests.get')
    def test_new_user_Google_validation(self, mock_get):
        # Nuevo usuario: Johana. Sin registros en base de datos ni caché
        self.authManager.user_service.delete(self.johana.userId)
        
        json = {
            'email': self.johana.username,
            'email_verified': "false",
            "expires_in": "3567",
            "avatar_url": "https://www.google.com/authentic/userinfo.email"
        }
        headers = {'Authorization': f"Bearer {self.johana.token}"}
        self.mock_response(mock_get, self.john.identity_provider.tokenValidationUrl,
            json)

        response = self.client.post('/api/validate-creds', json={
            'username': self.johana.username,
            'token': self.johana.token,
            'identity_provider_id': self.johana.identityProviderId
        })
        
        # Validar el request con los parámetros correctos
        mock_get.assert_called_once_with(
            self.johana.identity_provider.tokenValidationUrl,
            headers=headers)

        # Validar el token de Johana y su información en caché y en base de datos
        self.mock_asserts(response, 201, {"message": "User registered!"}, self.johana.username, self.johana.token)
    
    @patch('src.infraestructure.adapters.outbound.oauth.requests.get')
    def test_new_user_GitHub_validation(self, mock_get):
        # Nuevo usuario: Johana. Sin registros en base de datos ni caché
        self.authManager.user_service.delete(self.johana.userId)

        # Define a mock response object with the attributes you need
        json = {
            'login': self.johana.username,
            'id': "true",
            "nodid": "3568",
            "avatar_url": "https://www.github.com/auth/userinfo.email"
        }
        headers = {'Authorization': f"Bearer {self.johana.token}"}
        self.mock_response(mock_get, self.johana.identity_provider.tokenValidationUrl,
            json)

        response = self.client.post('/api/validate-creds', json={
            'username': self.johana.username,
            'token': self.johana.token,
            'identity_provider_id': self.johana.identityProviderId
        })
        
        # Validar el request con los parámetros correctos
        mock_get.assert_called_once_with(
            self.johana.identity_provider.tokenValidationUrl,
            headers=headers)

        # Validar el token de Johana y su información en caché y en base de datos
        self.mock_asserts(response, 201, {"message": "User registered!"}, self.johana.username, self.johana.token)

    @patch('src.infraestructure.adapters.outbound.oauth.requests.get')
    def test_existing_user_role_checks(self, mock_get):
        json = {
            'email': self.johana.username,
            'email_verified': "false",
            "expires_in": "3567",
            "avatar_url": "https://www.google.com/authentic/userinfo.email"
        }
        headers = {'Authorization': f"Bearer {self.johana.token}"}
        self.mock_response(mock_get, self.johana.identity_provider.tokenValidationUrl,
            json)

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
        roles_dict = response.json
        self.assertEqual(roles_dict[0]["name"], self.johana.roles[0].name)
        self.assertEqual(roles_dict[0]["description"], self.johana.roles[0].description)
        self.assertEqual(roles_dict[1]["name"], self.johana.roles[1].name)
        self.assertEqual(roles_dict[1]["description"], self.johana.roles[1].description)