import unittest
from src.root import Config, get_env_vars, app, db

# Objetivo: Ejecutar operaciones CRUD contra la base de datos de prueba
class TestConfig(unittest.TestCase):
    env = get_env_vars({"env": "tests", "type": "unit"})

    @classmethod
    def setUpClass(cls):
        # Este método se ejecuta una vez antes de todas las pruebas
        config = Config(cls.env)
        cls.app, cls.db = config.switch_db(app, db)
        
        # Crear un application context
        cls.app_context = cls.app.app_context()
        cls.app_context.push() 

        cls.db.drop_all()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def setUp(self):
        self.db.create_all()
        self.db.session.begin_nested()  # Comienza una transacción anidada

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()