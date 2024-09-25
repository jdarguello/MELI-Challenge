---
sidebar_position: 1
---

# Intro

El Ciclo de Vida del Desarrollo de Software (SDLC, por sus siglas en inglés) se trata de un framework que define las etapas de planeación y diseño de la __Arquitectura de Software__; definición de los estándares de _calidad_ y _seguridad_ del código mediante estrategias de _testing_; y definición de la estrategia de _packaging_ para las estrategias de deployment de artefactos en ambientes pre-productivos y productivos, como se resume en la Figura 1.

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

Para clonar el repositorio, ejecutamos el siguiente comando: 

```sh
git clone https://github.com/jdarguello/MELI-Challenge
```

El proyecto se compone de las siguientes carpetas principales:

* `.github`: pipelines CI/CD en GitHub Actions.
* `auth`: código fuente del microservicio.
* `docs`: documentación técnica del proyecto.
* `infraestructure`: archivos SQL base para la adecuación de las bases de datos, tanto para pruebas funcionales en _local_ como en _dev_. Además, contiene los archivos __Terraform__ para despliegue de recursos de infraestructura en AWS.


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

Ahora, deberías popular esta base de datos con información base para que puedas hacer pruebas de integración y de funcionalidades básicas, incluyendo flujos de _aprobación_ y _denegación_. Te puedes apoyar con los archivos pre-construidos que encontrarás en la carpeta `db_files`, dónde es sólo ejecutar los comandos SQL para adecuar la base de datos para testing. Los archivos los encontrarás en la siguiente ubicación.

```bash
/MELI-CHALLENGE
├── /.github
├── /assets
├── /infraestructure
│   ├── /db_files
|   |   ├── /init
|   |   |   └── init_schemes.sql
|   |   |   └── init_idps.sql
|   |   ├── /testing
|   |   |   └── init_app_users.sql
|   |   |   └── init_data.sql
|   |   |   └── super_user.sql
│   ├── main.py
│   ├── README.md
```

El orden de ejecución debería ser:

1. Habilitar los esquemas con `init_schemes.sql`. Con esto, la base de datos ya estará poblada con todas las tablas que necesita.
2. Habilitar los _proveedores de identidad_, Google y GitHub, ejecutando `init_idps.sql`.
3. Para tareas de testing, se puede poblar las tablas con información de ejemplo, empezando por `init_data.sql`, que contiene data genérica pre-configurada (algunos permisos, tipos, scopes y roles por default).
4. Si se desea, podremos poblar la base de datos con usuarios de ejemplo. Para ello, ejecutar: `init_app_users.sql`. Adicional, si se desea darles permisos de _super user_, ejecutar `super_user.sql`.

### 1.3. Caché

Dada la complejidad de la información a almacenar en caché, se decidió implementar una solución basada en __Redis__. Similar a la base de datos PostgreSQL, inicializaremos un contenedor con Redis de la siguiente forma.

```sh
docker run -d --name redis_MeLi -p 6379:6379 -it redis/redis-stack:latest
```

### 1.4. Contenedor local

Puedes generar un contenedor de este desarrollo en local con Docker. En primera instancia, tendrás que clonar el repositorio, acorde a lo establecido en el capítulo 1.1. Luego, en la carpeta `auth`, generas el _build_ de la siguiente forma:

```sh
docker build -t meli .
```

Con ello, crearemos la imagen docker, llamada _"meli"_. Puedes crear un contenedor de este proyecto ejecutando:

```sh
docker run -d --name meli-micro -p 5000:5000 meli
```

Para el desarrollo de pruebas contenerizadas, se recomienda que se cree el contenedor dentro de un Clúster de Kubernetes. Ver más detalles en la sección __[Cloud Native](../cloud/intro.md)__. 


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
