from flask import Flask
import yaml

# Lectura de variables de entorno
def get_env():
    with open("src/resources.yaml", "r") as f:
        return yaml.safe_load(f)

# Construcción de la aplicación y conexión con infraestructura
def create_app():
    app = Flask(__name__)
    return app
