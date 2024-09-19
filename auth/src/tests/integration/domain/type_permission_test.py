import unittest
from src.root import Config, get_env_vars, app, db
from src.domain.entities.type import Type
from src.domain.entities.permission import Permission

# Objetivo: Ejecutar operaciones CRUD contra la base de datos de prueba
class TestTypePermission(unittest.TestCase):

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

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def setUp(self):
        self.db.create_all()  # Crea todas las tablas en la base de datos
        self.db.session.begin_nested()  # Comienza una transacción anidada

        # Crea dos instancia de Permission y la almacena en la BD
        self.create_permission = Permission(kind='Create')
        self.db.session.add(self.create_permission)
        self.db.session.commit()

        self.read_permission = Permission(kind='Read')
        self.db.session.add(self.read_permission)
        self.db.session.commit()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def test_create_type_enroll_one_permission(self):
        # Crea una instancia de Type y la almacena en la BD
        vp_type = Type(name='VP Marketing', description='Vicepresidente de mercadeo', weight=1000)
        vp_type.permissions.append(self.create_permission)
        self.db.session.add(vp_type)
        self.db.session.commit()

        # Verifica que la instancia se haya guardado correctamente
        saved_type = db.session.get(Type, vp_type.typeId)
        self.assertEqual(saved_type.name, vp_type.name)
        self.assertEqual(saved_type.description, vp_type.description)
        self.assertEqual(saved_type.weight, vp_type.weight)
        self.assertEqual(len(saved_type.permissions), 1)
        self.assertEqual(saved_type.permissions[0].kind, self.create_permission.kind)
    
    def test_create_type_enroll_two_permissions(self):
        # Crea una instancia de Type y la almacena en la BD
        presiedent = Type(name='Presidente', description='Presidente corporativo', weight=1100)
        presiedent.permissions.append(self.create_permission)
        presiedent.permissions.append(self.read_permission)
        self.db.session.add(presiedent)
        self.db.session.commit()

        # Verifica que la instancia se haya guardado correctamente
        saved_type = db.session.get(Type, presiedent.typeId)
        self.assertEqual(saved_type.name, presiedent.name)
        self.assertEqual(saved_type.description, presiedent.description)
        self.assertEqual(saved_type.weight, presiedent.weight)
        self.assertEqual(len(saved_type.permissions), 2)

    def test_create_two_rolls_one_permission(self):
        # Crea una instancia de Type y la almacena en la BD
        vice = Type(name='Vice Presidente', description='Vice Presidente corporativo', weight=1000)
        vice.permissions.append(self.create_permission)
        self.db.session.add(vice)
        self.db.session.commit()

        # Crea otra instancia de Type y la almacena en la BD
        mensajero = Type(name='Mensajero', description='Mensajero')
        mensajero.permissions.append(self.create_permission)
        self.db.session.add(mensajero)
        self.db.session.commit()

        # Verifica que la instancia se haya guardado correctamente
        saved_types = db.session.query(Type).all()
        self.assertEqual(len(saved_types), 2)
        self.assertEqual(saved_types[0].name, vice.name)
        self.assertEqual(saved_types[1].name, mensajero.name)
        self.assertEqual(len(saved_types[0].permissions), 1)
        self.assertEqual(len(saved_types[1].permissions), 1)
        self.assertEqual(saved_types[0].permissions[0].kind, self.create_permission.kind)
        self.assertEqual(saved_types[1].permissions[0].kind, self.create_permission.kind)
    

if __name__ == '__main__':
    unittest.main()