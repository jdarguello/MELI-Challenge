---
sidebar_position: 1
---

# Intro

En la presente documentación, encontrarás todas las consideraciones técnicas en términos de __Arquitectura de Software__ de cada uno de los microservicios.

## Requerimientos Base

Respecto a lo definido en la guía `IAM - Challenge TL Backend.pdf`, se extraen los requerimientos enumerados a continuación.

### Funcionales

* Endpoint que genere un nuevo permiso. Debe incluir:
    * Nombre
    * Descripción
    * Tipo
    * Scope
* Endpoint que permita modificar atributos de un rol.
* Endpoint que permita consultar los roles disponibles.
* Endpoint que permita asociar un rol (permiso) con un usuario.
* Integración con OAuth/IDP para Autenticación Multi-Factor.

### No-Funcionales

* Lenguaje base: Golang (Chi o Gorilla Mux) o Python (Flask).
* Manejo de ambientes CI/CD.
* Integración con OAuth/IDP
