---
sidebar_position: 1
---

# Consideraciones

La generación del artefacto debe alinearse con la estrategia de contenerización de la apalicación a través de Kubernetes. Es por ello que se emplea Docker como sistema de orquestación de microservicios. En la sección introductoria, se especifica la forma de generar y consumir la imagen Docker mediante el Dockerfile, cuyo diseño se explica en detalle en la sección de [seguridad](./seguridad.md). 

Se empleó DockerHub como registro oficial de imágenes para el reto, debido a que tomó una decisión de testing en ambiente de desarrollo a través de ambientes efímeros (no permanentes) en AWS, por lo que al eliminarse la cuenta, eliminaría registries como ECR, por lo que se perdería la trazabilidad de las imágenes generadas.