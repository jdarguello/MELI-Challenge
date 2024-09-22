from src.tests.testconfig import TestConfig
from src.domain.entities.type import Type

# Objetivo: Ejecutar operaciones CRUD contra la base de datos de prueba
class TestType(TestConfig):
    def setUp(self):
        super().setUp()
        self.new_type = Type(name='Some name', description='Some description', weight=123)

    def test_create_type(self):
        # Crea una instancia de Type y la almacena en la BD
        self.db.session.add(self.new_type)
        self.db.session.commit()

        # Verifica que la instancia se haya guardado correctamente
        saved_type = self.db.session.get(Type, self.new_type.typeId)
        self.assertEqual(saved_type.name, 'Some name')
        self.assertEqual(saved_type.description, 'Some description')
        self.assertEqual(saved_type.weight, 123)
    
    def test_serialize_and_deserialize_type(self):
        # Crea una instancia de Type y la almacena en la BD
        self.db.session.add(self.new_type)
        self.db.session.commit()

        # Serializa la instancia y verifica que los valores coincidan
        serialized_type = self.new_type.to_dict()
        self.assertEqual(serialized_type['name'], 'Some name')
        self.assertEqual(serialized_type['description'], 'Some description')
        self.assertEqual(serialized_type['weight'], 123)

        # Deserializa la instancia y verifica que los valores coincidan
        deserialized_type = Type.from_dict(serialized_type)
        self.assertEqual(deserialized_type.name, 'Some name')
        self.assertEqual(deserialized_type.description, 'Some description')
        self.assertEqual(deserialized_type.weight, 123)