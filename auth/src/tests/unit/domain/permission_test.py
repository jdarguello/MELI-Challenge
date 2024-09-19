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