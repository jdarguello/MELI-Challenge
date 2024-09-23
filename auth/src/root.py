from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
import yaml

# Inicialización de la aplicación y servicios externos (bd, cache, etc)

# Configuración de la aplicación y base de datos
class Config:
    def __init__(self, env):
        print(env)
        self.TESTING = env["testing"]
        self.SQLALCHEMY_DATABASE_URI = env["db"]["uri"]
        self.SQLALCHEMY_TRACK_MODIFICATIONS = env["track_modifications"]
        self.SECRET_KEY = env["db"]["secret"]

        self.cache = None
        if "cache" in env:
            self.cache = {
                "host": env["cache"]["host"],
                "port": env["cache"]["port"],
                "db": env["cache"]["db"],
            }
    
    # Inicialización
    def setup(self):
        app = Flask(__name__)
        app.config.from_object(self)
        db = SQLAlchemy(app)
        cache = self.setup_cache()
        return app, db, cache
    
    def setup_cache(self):
        if self.cache is None:
            return None
        return redis.Redis(**self.cache)

    # Cambio de configuración de la base de datos
    def switch_db(self, app, db):
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
def get_env_vars(variables=None):
    args = get_env()
    if variables is None:
        variables = args["config"]
    if variables["env"] != "prod":
        return set_env_vars(args, variables, "cache" in args[variables["env"]][variables["type"]])
    return args["prod"]

def set_env_vars(args, variables, cache):
    db_args = args[variables["env"]][variables["type"]]["db"]
    if cache:
        cache_args = args[variables["env"]][variables["type"]]["cache"]
    for arg in ["unit", "integration", "functional"]:
        args[variables["env"]].pop(arg)
    args[variables["env"]]["db"] = db_args
    if cache:
        args[variables["env"]]["cache"] = cache_args
    return args[variables["env"]]

# Inicialización de la aplicación y de la base de datos
app, db, cache = Config(get_env_vars()).setup()