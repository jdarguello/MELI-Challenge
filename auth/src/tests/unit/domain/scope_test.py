from src.tests.testconfig import TestConfig
from src.domain.entities.scope import Scope

# Objetivo: Ejecutar operaciones CRUD contra la base de datos de prueba
class TestScope(TestConfig):
    def test_create_scope(self):
        # Crea una instancia de Scope y la almacena en la BD
        new_scope = Scope(name='Some name', description='Some description')
        self.db.session.add(new_scope)
        self.db.session.commit()

        # Verifica que la instancia se haya guardado correctamente
        saved_scope = self.db.session.get(Scope, new_scope.scopeId)
        self.assertEqual(saved_scope.name, 'Some name')
        self.assertEqual(saved_scope.description, 'Some description')