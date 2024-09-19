import unittest
from src.root import Config, get_env_vars, app, db
from src.domain.services.identity_provider import IdentityProvider

# Objetivo: Ejecutar operaciones CRUD contra la base de datos de prueba
class TestIdentityProvider(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Este método se ejecuta una vez antes de todas las pruebas
        env = get_env_vars({"env": "tests", "type": "unit"})
        config = Config(env)
        cls.app, cls.db = config.switchDB(app, db)
        
        # Crear un application context
        cls.app_context = cls.app.app_context()
        cls.app_context.push() 

        # Ahora, podemos interactuar con la base de datos
        cls.db.drop_all()
        cls.db.create_all()  # Crea todas las tablas en la base de datos

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def setUp(self):
        self.db.session.begin_nested()  # Comienza una transacción anidada

    def tearDown(self):
        self.db.session.rollback()  # Deshace los cambios en la base de datos

    def test_create_identityProvider(self):
       # Create an instance of IdentityProvider with all required fields
        new_identityProvider = IdentityProvider(
            clientId='test_client_id',
            name='Test Identity Provider',
            clientSecret='test_client_secret',
            baseUrl='https://example.com/base',
            tokenUrl='https://example.com/token',
            authorizationUrl='https://example.com/authorize',
            redirectUrl='https://example.com/redirect'
        )
        
        # Add the instance to the session and commit it
        db.session.add(new_identityProvider)
        db.session.commit()

        # Retrieve the instance from the database using its primary key
        saved_identityProvider = db.session.get(IdentityProvider, new_identityProvider.identityProviderId)
        
        # Verify that the saved instance matches the original values
        self.assertIsNotNone(saved_identityProvider)
        self.assertEqual(saved_identityProvider.clientId, 'test_client_id')
        self.assertEqual(saved_identityProvider.name, 'Test Identity Provider')
        self.assertEqual(saved_identityProvider.clientSecret, 'test_client_secret')
        self.assertEqual(saved_identityProvider.baseUrl, 'https://example.com/base')
        self.assertEqual(saved_identityProvider.tokenUrl, 'https://example.com/token')
        self.assertEqual(saved_identityProvider.authorizationUrl, 'https://example.com/authorize')
        self.assertEqual(saved_identityProvider.redirectUrl, 'https://example.com/redirect')

if __name__ == '__main__':
    unittest.main()