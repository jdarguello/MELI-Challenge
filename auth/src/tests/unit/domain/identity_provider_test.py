from src.tests.testconfig import TestConfig
from src.domain.services.identity_provider import IdentityProvider

# Objetivo: Ejecutar operaciones CRUD contra la base de datos de prueba
class TestIdentityProvider(TestConfig):
    def test_create_identityProvider(self):
       # Create an instance of IdentityProvider with all required fields
        new_identity_provider = IdentityProvider(
            clientId='test_client_id',
            name='Test Identity Provider',
            clientSecret='test_client_secret',
            baseUrl='https://example.com/base',
            tokenUrl='https://example.com/token',
            authorizationUrl='https://example.com/authorize',
            redirectUrl='https://example.com/redirect'
        )
        
        # Add the instance to the session and commit it
        self.db.session.add(new_identity_provider)
        self.db.session.commit()

        # Retrieve the instance from the database using its primary key
        saved_identity_provider = self.db.session.get(IdentityProvider, new_identity_provider.identityProviderId)
        
        # Verify that the saved instance matches the original values
        self.assertIsNotNone(saved_identity_provider)
        self.assertEqual(saved_identity_provider.clientId, 'test_client_id')
        self.assertEqual(saved_identity_provider.name, 'Test Identity Provider')
        self.assertEqual(saved_identity_provider.clientSecret, 'test_client_secret')
        self.assertEqual(saved_identity_provider.baseUrl, 'https://example.com/base')
        self.assertEqual(saved_identity_provider.tokenUrl, 'https://example.com/token')
        self.assertEqual(saved_identity_provider.authorizationUrl, 'https://example.com/authorize')
        self.assertEqual(saved_identity_provider.redirectUrl, 'https://example.com/redirect')