import unittest
from src.root import Config, get_env_vars, app, db
from src.domain.entities.type import Type

# Objetivo: Ejecutar operaciones CRUD contra la base de datos de prueba
class TestType(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Este método se ejecuta una vez antes de todas las pruebas
        env = get_env_vars({"env": "tests", "type": "unit"})
        config = Config(env)
        cls.app, cls.db = config.switch_db(app, db)
        
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

    def test_create_type(self):
        # Crea una instancia de Type y la almacena en la BD
        new_type = Type(name='Some name', description='Some description', weight=123)
        self.db.session.add(new_type)
        self.db.session.commit()

        # Verifica que la instancia se haya guardado correctamente
        saved_type = db.session.get(Type, new_type.typeId)
        self.assertEqual(saved_type.name, 'Some name')
        self.assertEqual(saved_type.description, 'Some description')
        self.assertEqual(saved_type.weight, 123)

if __name__ == '__main__':
    unittest.main()