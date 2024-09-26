from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from dotenv import load_dotenv
import os
import re
import redis
import yaml

# Inicialización de la aplicación y servicios externos (bd, cache, etc)

# Configuración de la aplicación y base de datos
class Config:
    def __init__(self, env):
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

        self.CSRF_SECRET = env["csrf-secret"]
    
    # Inicialización
    def setup(self):
        app = Flask(__name__)
        app.config['SECRET_KEY'] = self.CSRF_SECRET
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
    load_dotenv()
    with open("src/resources.yaml", "r") as f:
        return yaml.safe_load(f)
    
# Limpieza y definición de las variables de entorno para
# configuración de servicios externos
def get_env_vars(variables=None):
    args = get_env()
    if variables is None:
        variables = {
            "env": os.getenv("env"),
            "type": os.getenv("type")
        }
    if variables["env"] != "prod" and variables["type"] != "functional":
        return set_env_vars(args, variables, "cache" in args[variables["env"]][variables["type"]])
    return set_prod_vars(args, variables, True)

# Testing variables
def set_env_vars(args, variables, cache):
    db_args = args[variables["env"]][variables["type"]]["db"]
    if cache:
        cache_args = args[variables["env"]][variables["type"]]["cache"]
    if variables["env"] != "prod":
        for arg in ["unit", "integration", "functional"]:
            args[variables["env"]].pop(arg)
    args[variables["env"]]["db"] = db_args
    if cache:
        args[variables["env"]]["cache"] = cache_args
    return args[variables["env"]]

def set_prod_vars(args, variables, cache):
    args = set_env_vars(args, variables, cache)
    # Replace dynamic vars with env vars
    for section in ["db", "cache"]:
        for key, value in args[section].items():
            args[section][key] = replace_secrets(value)
    args["csrf-secret"] = replace_secrets(args["csrf-secret"])
    db = args["db"]
    db["uri"] = "postgresql://" + db["user"] + ":" + db["password"] + "@" + \
        db["host"] + "/" + db["database"]
    return args

def replace_secrets(value):
    splitted_value = value.split(" ")
    if len(splitted_value) > 1:
        return os.getenv(value.split(" ")[1])
    return value

# Inicialización de la aplicación y de la base de datos
app, db, cache = Config(get_env_vars()).setup()