import unittest
from src.root import Config, get_env_vars, app, db
from src.domain.entities.permission import Permission

# Objetivo: Ejecutar operaciones CRUD contra la base de datos de prueba
class TestPermission(unittest.TestCase):

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

    def test_create_permission(self):
        # Crea una instancia de Permission y la almacena en la BD
        new_permission = Permission(kind='Create')
        #print(new_permission.kind)
        db.session.add(new_permission)
        db.session.commit()

        # Verifica que la instancia se haya guardado correctamente
        saved_permission = db.session.get(Permission, new_permission.permissionId)
        self.assertEqual(saved_permission.kind, 'Create')

if __name__ == '__main__':
    unittest.main()