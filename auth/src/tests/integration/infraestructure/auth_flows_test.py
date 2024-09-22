from src.tests.integration.infraestructure.testconfig_infr import TestConfigInfraestructure

class TestAuthFlows(TestConfigInfraestructure):
    def setUp(self):
        super().setUp()

    def test_login(self):
        self.cache.set('key', 'value')
        self.assertEqual(self.cache.get('key'), b'value')

    def test_logout(self):
        self.cache.set('key2', 'value')
        self.assertEqual(self.cache.get('key2'), b'value')
    