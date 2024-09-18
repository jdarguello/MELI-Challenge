import unittest
from src.root import *
from src.domain.entities.type import Type
import os

# Objetivo: Ejecutar operaciones CRUD contra la base de datos de prueba
class TestType(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Este método se ejecuta una vez antes de todas las pruebas
        env = get_env_vars({"env": "tests", "type": "unit"})
        config = Config(env)
        cls.app, cls.db = config.switchDB(app, db)
        
        # Create an application context
        cls.app_context = cls.app.app_context()
        cls.app_context.push()  # Push the app context to make it active


        # Now you can interact with the database
        cls.db.create_all()  # Create all tables in the database

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()
        # Este método se ejecuta una vez después de todas las pruebas
        #cls.db.session.remove()
        #cls.db.drop_all()  # Elimina todas las tablas de la base de datos

    def setUp(self):
        self.db.session.begin_nested()  # Comienza una transacción anidada

    def tearDown(self):
        self.db.session.rollback()  # Deshace los cambios en la base de datos

    def test_create_type(self):
        # Crea una instancia de Type
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
