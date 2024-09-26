---
sidebar_position: 4
---

# Métricas de calidad

Para la evaluación continua de métricas de calidad, se empleó __SonarCloud__, herramienta que ejecuta _análisis estático de código_ con base en las métricas de cobertura de pruebas unitarias y de integración. SonarCloud es una de las herramientas más robustas en la industria por su alta cobertura de métricas mediante _Quality Gates_. Entre las métricas más populares están:

* __Cobertura:__ cantidad de líneas de código ejecutadas en los flujos de test unitarios y de integración comparadas con la cantidad total existente en el algoritmo.
* __Code Smells:__ sintaxis inadecuada dentro del código; ya sea por nombres de variables y variables no utilizadas en la lógica, entre otrs.
* __Duplication Lines:__ cantidad de líneas idénticas en el código. Mide la cantidad de _copy-paste_ que se haya hecho durante la construcción del algoritmo.
* __Seguridad:__ durante el análisis, Sonar también valida ciertas consideraciones de seguridad que puedan suponer un riesgo, como la presencia de secretos en el código fuente, por ejemplo.

A continuación, se presenta un screenshot de algunos de los resultados más recientes.

<img src="../../../img/sdlc/pruebas/sonar.png" width="1500px" />

Figura 13. Resultados en SonarCloud.

Como se evidencia, Sonar informa los siguientes resultados:

* 0 recomendaciones de seguridad, por lo que no hay riesgos de presencia de información sensible en el código fuente.
* 96.8% de cobertura.
* 1.3% de duplicidad de líneas de código.
* 16 issues de mantenibilidad por _code smells_.

En general, son resultados muy positivos que resaltan una alta calidad y buenas prácticas de desarrollo. 