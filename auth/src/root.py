from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import yaml

# Inicialización de la aplicación y servicios externos (bd, cache, etc)

# Configuración de la base de datos
class DBConfig:
    def __init__(self, env):
        self.TESTING = env["testing"]
        self.SQLALCHEMY_DATABASE_URI = env["db"]["uri"]
        self.SQLALCHEMY_TRACK_MODIFICATIONS = env["track_modifications"]
        self.SECRET_KEY = env["db"]["secret"]

# Lectura de variables de entorno
def get_env():
    with open("src/resources.yaml", "r") as f:
        return yaml.safe_load(f)

# Limpieza y definición de las variables de entorno para
# configuración de servicios externos
def get_env_vars():
    args = get_env()
    vars = args["config"]
    if not vars["env"] == "prod":
        db_args = args[vars["env"]][vars["type"]]["db"]
        for arg in ["unit", "integration", "functional"]:
            args[vars["env"]].pop(arg)
        args[vars["env"]]["db"] = db_args
        return args[vars["env"]]
    return args["prod"]

# Inicialización de la aplicación y de la base de datos
app = Flask(__name__)
app.config.from_object(DBConfig(get_env_vars()))
db = SQLAlchemy(app)