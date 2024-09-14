---
sidebar_position: 1
---

# Generalidades

Una Arquitectura de Software bien establecida se caracteriza por tener capas (layers) definidas que separan la lógica de negocio con las integraciones entre tecnologías para facilitar la mantenibilidad. Debido a ello, se ha decidido implementar una _arquitectura hexagonal_ para estructurar las capas del microservicio.

Esta decisión de arquitectura, por sí misma, no es suficiente para garantizar la calidad ni la mantenibilidad de la aplicación a futuro. Debe complementarse con las prácticas de _clean architecture_ para alcanzar ese fin, principalmente: principios SOLID, TDD y DDD.


## Arquitectura Hexagonal

La arquitecrtura hexagonal estructura la aplicación en tres capas:

* __Domain:__ contiene la lógica de negocio, definida a través de _entidades_ y _casos de uso_.
* __Application:__ interfaz que abstrae la interacción entre el dominio y el mundo exterior.
* __Infraestructure:__ sistemas externos y servicios, como bases de datos, brókers de mensajería y API's externos.

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs>
    <TabItem value="esquema" label="Esquema" default>
        ![](../../../static/img/sdlc/arquitectura/hexagonal.png)
        <p>Figura 2. Capas distribuidas en la Arquitectura Hexagonal.</p>
    </TabItem>
    <TabItem value="estructura" label="Estructura">
        Estructura base de un microservicio en Flask basado en arquitectura hexagonal.
        ```bash
        /my_microservice
        ├── /src
        │   ├── /application
        │   │   ├── /ports
        │   │   │   ├── /inbound
        │   │   │   │   └── some_inbound_port.py
        │   │   │   ├── /outbound
        │   │   │   │   └── some_outbound_port.py
        │   │   └── /usecases
        │   │       └── some_use_case.py
        │   ├── /domain
        │   │   ├── /entities
        │   │   │   └── some_domain_entity.py
        │   │   ├── /services
        │   │   │   └── some_domain_service.py
        │   │   ├── /exceptions
        │   │   │   └── some_domain_exception.py
        │   ├── /infrastructure
        │   │   ├── /adapters
        │   │   │   ├── /inbound
        │   │   │   │   └── some_inbound_adapter.py
        │   │   │   ├── /outbound
        │   │   │   │   └── some_outbound_adapter.py
        │   │   ├── /persistence
        │   │   │   └── some_repository.py
        │   │   ├── /messaging
        │   │   │   └── some_messaging_service.py
        │   │   ├── /config
        │   │   │   └── config.py
        │   ├── /web
        │   │   ├── /controllers
        │   │   │   └── some_controller.py
        │   │   ├── /schemas
        │   │   │   └── some_schema.py
        ├── /tests
        │   ├── /unit
        │   ├── /integration
        │   └── /contract
        ├── /venv  (for virtual environment)
        ├── main.py  (entry point to start the app)
        └── requirements.txt
        ```
    </TabItem>
</Tabs>
