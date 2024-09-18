from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import yaml

# Inicialización de la aplicación y servicios externos (bd, cache, etc)

# Configuración de la aplicación y base de datos
class Config:
    def __init__(self, env):
        self.TESTING = env["testing"]
        self.SQLALCHEMY_DATABASE_URI = env["db"]["uri"]
        self.SQLALCHEMY_TRACK_MODIFICATIONS = env["track_modifications"]
        self.SECRET_KEY = env["db"]["secret"]
    
    # Inicialización
    def setUp(self):
        app = Flask(__name__)
        app.config.from_object(self)
        db = SQLAlchemy(app)
        return app, db

    # Cambio de configuración de la base de datos
    def switchDB(self, app, db):
        with app.app_context():
            app.config.from_object(self)
            db.session.remove()
            db.engine.dispose()
        return app, db

# Lectura de variables de entorno
def get_env():
    with open("src/resources.yaml", "r") as f:
        return yaml.safe_load(f)
    


# Limpieza y definición de las variables de entorno para
# configuración de servicios externos
def get_env_vars(vars=None):
    args = get_env()
    if vars is None:
        vars = args["config"]
    if not vars["env"] == "prod":
        db_args = args[vars["env"]][vars["type"]]["db"]
        for arg in ["unit", "integration", "functional"]:
            args[vars["env"]].pop(arg)
        args[vars["env"]]["db"] = db_args
        return args[vars["env"]]
    return args["prod"]

# Inicialización de la aplicación y de la base de datos
app, db = Config(get_env_vars()).setUp()