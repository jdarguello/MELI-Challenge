from src.tests.testconfig import TestConfig
from src.domain.entities.scope import Scope

# Objetivo: Ejecutar operaciones CRUD contra la base de datos de prueba
class TestScope(TestConfig):
    def setUp(self):
        super().setUp()
        self.new_scope = Scope(name='Some name', description='Some description')
    
    def test_create_scope(self):
        # Crea una instancia de Scope y la almacena en la BD
        self.db.session.add(self.new_scope)
        self.db.session.commit()

        # Verifica que la instancia se haya guardado correctamente
        saved_scope = self.db.session.get(Scope, self.new_scope.scopeId)
        self.assertEqual(saved_scope.name, 'Some name')
        self.assertEqual(saved_scope.description, 'Some description')
    
    def test_serialize_and_deserialize_scope(self):
        # Crea una instancia de Scope y la almacena en la BD
        self.db.session.add(self.new_scope)
        self.db.session.commit()

        # Serializa la instancia y verifica que los valores coincidan
        serialized_scope = self.new_scope.to_dict()
        self.assertEqual(serialized_scope['name'], 'Some name')
        self.assertEqual(serialized_scope['description'], 'Some description')

        # Deserializa la instancia y verifica que los valores coincidan
        deserialized_scope = Scope.from_dict(serialized_scope)
        self.assertEqual(deserialized_scope.name, 'Some name')
        self.assertEqual(deserialized_scope.description, 'Some description')