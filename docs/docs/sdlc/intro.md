---
sidebar_position: 1
---

# Intro

El Ciclo de Vida del Desarrollo de Software (SDLC, por sus siglas en inglés) se trata de un framework que define las etapas de planeación y diseño de la __Arquitectura de Software__; definición de los estándares de _calidad_ y _seguridad_ del código mediante estrategias de _testing_; y definición de la estrategia de _packaging_ para las estrategias de deployment de artefactos en ambientes pre-productivos y productivos, como se resume en la siguiente Figura 1.

<img src="../../img/SDLC.png" width="300px" />

Figura 1. Etapas del Ciclo de Vida del Desarrollo de Software.

## 1. Ambiente Local

Para generar el ambiente local que permita correr el desarrollo en un ordenador, debes tener instalado lo siguiente:

* Git
* Python 3.12
* Node.js v20.17.0
* DBeaver v24.2
* Docker

Para la ejecución de este proyecto en local, puedes hacerlo o _clonando el repositorio_ o generando un contenedor con Docker o Podman.

### 1.1. Clonar el repositorio

Lo primero es clonar el repositorio


### 1.2. Bases de Datos

Para el desarrollo del microservicio, se utilizaron dos tipos de bases de datos.

1. __SQLite:__ se emplea para la ejecución de los _test unitarios_ y _test de integración_. Sirve para evaluar las operaciones de persistencia sobre la base de datos. No requiere de instalación de nigún paquete. Su configuración base está preconstruida dentro de la clase `TestConfig`. Para más detalles, ir a la página de [Pruebas Automatizadas](./calidad/pruebas.md).
2. __PostgreSQL:__ se emplea para ejecutar _test funcionales_. Se recomienda construirla mediante un contenedor Docker. 

#### 1.2.1. PostgreSQL

Para generar la base de datos, sólo debes ejecutar el siguiente comando:

```sh
docker run -d --name MeLi_db \
    -e POSTGRESQL_DATABASE=meli-challenge \
    -e POSTGRESQL_USERNAME=test_user \
    -e POSTGRESQL_PASSWORD=test123 \
    -p 5432:5432 \
    bitnami/postgresql:latest
```

Esta base de datos de pruebas ya está pre-configurada en la aplicación para ser utilizada. Para acceder a la base de datos en __DBeaver__, debes tener en cuenta los siguientes argumentos:

* __Database:__ meli-challenge
* __Port:__ 5432
* __Nombre de usuario:__ test_user
* __Contraseña:__ test123

Ahora, deberías popular esta base de datos con información base para que puedas hacer pruebas de integración y de funcionalidades básicas, incluyendo flujos de _aprobación_ y _denegación_. Te puedes apoyar con los archivos pre-construidos que encontrarás en la carpeta `db_files`, dónde es sólo copiar los comandos SQL y ejecutarlos en DBeaver. Los archivos `common_queries.sql` e `init_data.sql` los encontrarás en la siguiente ubicación.

```bash
/MELI-CHALLENGE
├── /.github
├── /assets
├── /auth
│   ├── /db_files
│   │   └── common_queries.sql
│   │   ├── init_data.sql
│   ├── /src
│   ├── main.py
│   ├── README.md
```

### 1.3. Caché

Dada la complejidad de la información a almacenar en caché, se decidió implementar una solución basada en __Redis__. Similar a la base de datos PostgreSQL, inicializaremos un contenedor con Redis de la siguiente forma.

```sh
docker run -d --name redis_MeLi -p 6379:6379 -it redis/redis-stack:latest
```

### 1.4. Contenedor local

Puedes generar un contenedor de este desarrollo en local con Docker. En primera instancia, tendrás que clonar el repositorio, acorde a lo establecido en el capítulo 1.1. Luego, sólo debes correr el siguiente comando.

```sh
docker run ...
```

Con esta configuración, el contenedor con la solución podrá comunicarse con la base de datos (ver 1.2) y con el caché (ver 1.3)


## 2. Requerimientos Base

Para el problema en cuestión, se han definido los requerimientos enumerados a continuación.

### 2.1. Funcionales

* Endpoint que genere un nuevo permiso. Debe incluir:
    * Nombre
    * Descripción
    * Tipo
    * Scope
* Endpoint que permita modificar atributos de un rol.
* Endpoint que permita consultar los roles disponibles.
* Endpoint que permita asociar un rol (permiso) con un usuario.
* Integración con OAuth/IDP para Autenticación Multi-Factor.

### 2.2. No-Funcionales

* Lenguaje base: Golang (Chi o Gorilla Mux) o Python (Flask).
* Manejo de ambientes CI/CD.
* Integración con OAuth/IDP
