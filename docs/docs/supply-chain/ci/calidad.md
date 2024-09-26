---
sidebar_position: 2
---

# Prácticas de calidad

Complementa a las definiciones realizadas en el capítulo de calidad del SDLC. El pipeline definido (`CI_quality.yaml`) sigue los siguientes pasos:

1. Descarga el código fuente del repositorio.
2. Instala Python.
3. Crea un contenedor Redis, para la ejecución de tests de integración.
4. Instala las dependencias Python.
5. Adecua las variables de entorno para la configuración de las pruebas unitarias y de integración.
6. Ejecuta las pruebas unitarias para la generación del reporte de cobertura.
7. Envía los resultados a SonarCloud para la centralización de métricas.

En paralelo, se ejecuta el pipeline de seguridad (`CI_secOps.yaml`), con el que se busca adelantar el escaneo de la imagen Docker del desarrollo. Sigue la siguiente metodología:

1. Descarga el código fuente.
2. Compila la imagen Docker
3. Ejecuta el escaneo con Trivy en busca de vulnerabilidades críticas y altas.

Si la ejecución de los dos pipelines es exitosa, procede con la generación y publicación del artefacto.