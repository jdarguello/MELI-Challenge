from src.tests.testconfig import TestConfig
from src.domain.entities.permission import Permission
from src.domain.entities.type import Type
from src.domain.entities.scope import Scope

class TestConfigDomain(TestConfig):
    def setUp(self):
        super().setUp()
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