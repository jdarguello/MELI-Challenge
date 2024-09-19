from src.tests.testconfig import TestConfig
from src.domain.entities.type import Type

# Objetivo: Ejecutar operaciones CRUD contra la base de datos de prueba
class TestType(TestConfig):
    def test_create_type(self):
        # Crea una instancia de Type y la almacena en la BD
        new_type = Type(name='Some name', description='Some description', weight=123)
        self.db.session.add(new_type)
        self.db.session.commit()

        # Verifica que la instancia se haya guardado correctamente
        saved_type = self.db.session.get(Type, new_type.typeId)
        self.assertEqual(saved_type.name, 'Some name')
        self.assertEqual(saved_type.description, 'Some description')
        self.assertEqual(saved_type.weight, 123)