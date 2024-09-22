from src.tests.testconfig import TestConfig
from src.domain.entities.permission import Permission

# Objetivo: Ejecutar operaciones CRUD contra la base de datos de prueba
class TestPermission(TestConfig):
    def test_create_permission(self):
        # Crea una instancia de Permission y la almacena en la BD
        new_permission = Permission(kind='Create')
        self.db.session.add(new_permission)
        self.db.session.commit()

        # Verifica que la instancia se haya guardado correctamente
        saved_permission = self.db.session.get(Permission, new_permission.permissionId)
        self.assertEqual(saved_permission.kind, 'Create')
    
    def test_serialize_and_deserialize_permission(self):
        # Crea una instancia de Permission y la almacena en la BD
        new_permission = Permission(kind='Read')
        self.db.session.add(new_permission)
        self.db.session.commit()

        # Serializa la instancia y verifica que los valores coincidan
        serialized_permission = new_permission.to_dict()
        self.assertEqual(serialized_permission['kind'], 'Read')

        # Deserializa la instancia y verifica que los valores coincidan
        deserialized_permission = Permission.from_dict(serialized_permission)
        self.assertEqual(deserialized_permission.kind, 'Read')