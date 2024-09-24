# Imagen minimalista
FROM python:3.12-alpine

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
CMD ["python3", "main.py", "--host=0.0.0.0"]
#CMD ["gunicorn", "-w", "4", "-t", "2", "-b", "0.0.0.0:5000", "src.root:app"]