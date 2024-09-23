from src.tests.integration.infraestructure.testconfig_infr import TestConfigInfraestructure
from src.application.usecases.authManager import AuthManager
from unittest.mock import MagicMock, patch
import unittest
import json

class TestAdminFlows(TestConfigInfraestructure):
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
    
    @patch('src.infraestructure.adapters.outbound.oauth.requests.get')
    def test_valid_admin_create_idp_that_already_exists(self, mock_get):
        # Define a mock response object with the attributes you need
        headers = {'Authorization': f"Bearer {self.json['token']}"}
        self.mock_response(mock_get, self.john.identity_provider.tokenValidationUrl,
            json)

        response = self.client.post('/api/admin/idp',  json={
            "clientId": "1ei3nj32",
            "name": "Twitter",
            "clientSecret": "e32jn4j24km5k45n4",
            "tokenValidationUrl": "https://api.twitter.com/1.1/account/verify_credentials.json",
            "tokenExpiryTime": 3600
        }, headers={
                'token': self.john.token,
                'username': self.john.username,
                'identity_provider_id': self.john.identityProviderId
            })

        # Validar el request con los parámetros correctos (sin idp, con caché)
        mock_get.assert_not_called()

        # Validar que el idp haya sido creado
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Identity Provider already exists"})
    
    def test_regular_user_create_idp(self):
        #New user, zero permissions
        nicolas = self.authManager.user_service.create(
            username="nico123",
            token="eyeyeyey123e34",
            identity_provider_id=1
        )

        # Register in cache
        self.authManager.register_user_in_cache(nicolas)

        response = self.client.post('/api/admin/idp',  json={
            "clientId": "1ei3nj32",
            "name": "TikTok",
            "clientSecret": "e32jn4j24km5k45n4"}, headers={
                'token': nicolas.token,
                'username': nicolas.username,
                'identity_provider_id': nicolas.identityProviderId
            })

        self.assertEqual(response.json, {"message": "Forbidden: you don't have a role with enough permissions."})
        self.assertEqual(response.status_code, 403)

    def test_admin_update_idp_that_already_exists(self,):
        response = self.client.put('/api/admin/idp', json={
            "clientId": "jsjsjdndiw",
            "name": "Twitter",
            "clientSecret": "eyeyeyeyeyeye",
        }, headers={
                'token': self.john.token,
                'username': self.john.username,
                'identity_provider_id': self.john.identityProviderId
            })

        self.assertEqual(response.status_code, 200)
        idp_json = response.json
        self.assertEqual(idp_json["name"], "Twitter")
        idp = self.authManager.identity_provider_service.get_by_name("Twitter")
        self.assertEqual(idp.clientId, "jsjsjdndiw")
        self.assertEqual(idp.clientSecret, "eyeyeyeyeyeye")
    