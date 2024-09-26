---
sidebar_position: 2
---

# Condiciones de seguridad

Las decisiones sobre el diseño de ciberseguridad de un software se aplican, incluso, dentro del ciclo de vida del deasarrollo. La generación del artefacto es una de las etapas más críticas, y más tratándose de un contenedor, como se aprecia en la Figura 15. 

<img src="../../../img/sdlc/artefacto/container.png" width="400px" />

Figura 15. Estructura de un contenedor.

## Dockerfile

Un contenedor se trata de un paquete de software que contiene su propio sistema operativo, pero que consume recursos propios del servidor. Muchas veces, se concibe como una unidad _"aislada"_ dentro del funcionamiento de una aplicación basada en microservicios y se ejecuta como un proceso dentro del kernel del servidor. Lo que significa que si un hacker accede al contenedor, puede también, en consecuencia, vulnerar el kernel y manipular todos los demás procesos que se orquestan a voluntad. Es por ello que es altamente importante que a nivel de _Dockerfile_, el usuario maestro del contenedor tenga únicamente los permisos necesarios para la ejecución de su labor.

Adicional, la imagen base del contenedor debe tener también los paquetes de software mínimament necesarios. Teniendo eso en mente, se propuso el siguiente Dockerfile:

```dockerfile
# Imagen minimalista
FROM python:3.12-alpine as build

# Instalación de dependencias, incluyendo los archivos de desarrollo de PostgreSQL
RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories && \
    echo "https://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories

# Update the package index and install dependencies
RUN apk update && apk add --no-cache \
    curl \
    g++ \
    gcc \
    musl-dev \
    postgresql-dev

# Usuario no-root para garantizar estándares de seguridad
ENV HOME=/home/appuser
ENV PATH="/home/appuser/.local/bin:${PATH}"
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser

# Archivos de la aplicación y configuración para lectura de dependencias del usuario no-root
WORKDIR /home/appuser
COPY . /home/appuser
RUN pip install --user --no-cache-dir -r requirements.txt

# Correr la aplicación
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-t", "2", "-b", "0.0.0.0:5000", "src.root:app"]
```

Como se puede observar, la imagen base es de tipo `python:alpine`, que es altamente minimalista. Se gestionó un GID (GroupID) y un UID (UserID) con permisos mínimos.

## Gunicorn

Una de las principales consideraciones de seguridad a la hora de construir un microservicio con Flask es el de usar un servidor de aplicación tipo WSGI, por lo que empleamos Gunicorn como servidor oficial del microservicio.