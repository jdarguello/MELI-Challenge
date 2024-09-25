---
sidebar_position: 3
---

# Pruebas Automatizadas

Como se mencionó anteriormente, las pruebas unitarias y de integración fueron ejecutadas con las librerías `unittest` y `pytest`. Siendo un Flask un micro-framework de desarrollo web, no presenta por sí mismo una arquitectura base, a diferencia de otros frameworks como _Django_ o _Spring Boot_, en Java.

Con base en la arquitectura diseñada, se decidió elaborar dos clases de configuración y centralización de las configuraciones: `root.py` y `app.py`. La primera se centra en la conexión con las herramientas de [persistencia](../arquitectura/oauth.mdx) y [concurrecia](../arquitectura/oauth.mdx) de datos, mientras que la segunda gestiona los flujos propios del microservicio de forma centralizada. 

Se centralizó la configuración de conexión a los servicios de _bases de datos_ y _caché_ a través del archivo `resources.yaml`, que permite configurar con facilidad las conexiones a los servicios descritos. Para las pruebs de __funcionalidad__ en ambiente local, se habilitó la opción de tener un archivo `.env` con las gestión de variables de entorno. Un ejemplo del contenido de este archivo:

```yaml
env=tests
type=functional
DB_URI_TEST=postgresql://test_user:test123@localhost:5432/meli-challenge
DB_SECRET_TEST=secret
DB_HOST_TEST=localhost
DB_PORT_TEST=5432
DB_USER_TEST=test_user
DB_PASSWORD_TEST=test123
DB_DATABASE_TEST=meli-challenge
CACHE_HOST_TEST=localhost
CACHE_PORT_TEST=6379
CACHE_DB_TEST=1
```

Comparándolo con el archivo de `resources.yaml`, se puede apreciar que contiene los valores para conectarse a la base de datos y caché habilitados en los contenedores Docker locales. 

Todos los test unitarios y de integración los encontrarás en la siguiente ubicación: `auth/src/tests`

## Unit Tests

Los test unitarios buscan probar la funcionalidad aislada de clases y métodos. Al emplear una configuración de persistencia de datos con _arquitectura hexagonal_ y `SQLAlchemy`, como ORM, se centralizó la estrategia de este tipo de tests para corroborar la persistencia de los datos de la capa del dominio; así como sus procesos de __serialización__ y __deserialización__ para los procesos con caché. También, se construyeron múltiples pruebas unitarias para corroborar las funcionalidades base en las operaciones CRUD en la capa de persistencia en los servicios base, en la capa de `application`.

Para facilitar la mantenibilidad futura del código, se creó la clase base `testconfig.py`, que abstrae la lógica de conexión con la base de datos `SQLite` de pruebas en memoria. Esta clase base también usa el `root.py` para generar establecer la conexión de la base de datos y la configuración general de la aplicación Flask, como se aprecia a continuación.

```py
import unittest
from src.root import Config, get_env_vars, app, db

# Objetivo: Ejecutar operaciones CRUD contra la base de datos de prueba
class TestConfig(unittest.TestCase):
    env = get_env_vars({"env": "tests", "type": "unit"})

    @classmethod
    def setUpClass(cls):
        # Este método se ejecuta una vez antes de todas las pruebas
        config = Config(cls.env)
        cls.app, cls.db = config.switch_db(app, db)
        
        # Crear un application context
        cls.app_context = cls.app.app_context()
        cls.app_context.push() 

        cls.db.drop_all()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def setUp(self):
        self.db.create_all()
        self.db.session.begin_nested()  # Comienza una transacción anidada

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
```

Toda prueba unitaria elaborada emplea relaciones de herencia y polimorfismo con la clase `TestConfig`, o sus derivados, para extender su funcionalidad base.

## Integration Tests

Los test de integración buscan comprobar la funcionalidad entre múltiples componentes de software, ya sean internos o externos. Para este caso puntual, se empleó principalmente en corroborar la funcionalidad de los casos de uso principales: `UserService`, que contiene las integraciones principales con la capa de persistencia (dominio), `AuthManager`, que abstrae las funcionalidades base de autenticación contra caché y OAuth 2.0, tanto Google como GitHub, y `AuthDecorators` que simplifica la adopción de los métodos de _autenticación_ y _autorización_ mediante los métodos `auth_required` y `role_required`. 

Dado que OAuth 2.0 requiere el uso de un `ClientID` y `ClientSecrets` para conectarse con el _identity provider_, se tomó la decisión de crear __mocks__ sobre la comunicación con ellos para evitar fugas de información durante la ejecución de los tests en los pipelines de integración continua.

Así como en los _test unitarios_, los test de integración también cuentan con clases en la capa de `application` e `infraestructure` para comunicarse con la base de datos y el caché. Se destacan las clases `TestConfigApplication`, `TestConfigCache` y `TestConfigInfraestructure` que simplifican y unifican la creación de objetos comunes y configuraciones generales de mocks.