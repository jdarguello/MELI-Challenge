import unittest
from src.root import Config, get_env_vars, app, db
from src.domain.entities.type import Type
from src.domain.entities.permission import Permission
from src.domain.entities.role import Role
from src.domain.entities.scope import Scope

# Objetivo: Ejecutar operaciones CRUD contra la base de datos de prueba
class TestRoleTypeScope(unittest.TestCase):

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

        #Crea un Type, lo relaciona con el permiso Create y lo almacena en la BD
        self.admin = Type(name='Admin', description='Administrador', weight=1000)
        self.admin.permissions.append(self.create_permission)
        self.db.session.add(self.admin)
        self.db.session.commit()

        # Crea una instancia de Scope y la almacena en la BD
        self.corporate = Scope(name='Corporativo TI', description='Corporativo de Servicios de Tecnología')
        self.db.session.add(self.corporate)
        self.db.session.commit()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def test_create_type_enroll_one_permission(self):
        # Crea una instancia de Role, la relaciona con el scope Corporate, el Type Admin y la almacena en la BD
        vp_marketing = Role(name='VP Marketing', description='Vicepresidente de mercadeo')
        vp_marketing.type = self.admin
        vp_marketing.scope = self.corporate
        self.db.session.add(vp_marketing)
        self.db.session.commit()

        # Verifica que la instancia se haya guardado correctamente
        saved_role = db.session.get(Role, vp_marketing.roleId)
        self.assertEqual(saved_role.name, vp_marketing.name)
        self.assertEqual(saved_role.description, vp_marketing.description)
        self.assertEqual(saved_role.type.name, self.admin.name)
        self.assertEqual(saved_role.scope.name, self.corporate.name)

        #Además, verifica que el Role tenga permiso de Create
        self.assertEqual(len(saved_role.type.permissions), 1)
        self.assertEqual(saved_role.type.permissions[0].kind, self.create_permission.kind)
        
if __name__ == '__main__':
    unittest.main()