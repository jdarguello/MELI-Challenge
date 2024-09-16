# Dependencias generales
from flask import Flask
import yaml
# Dependencias del microservicio
from src.infraestructure.adapters.auth import AuthAdapter
from src.infraestructure.adapters.user import UserAdapter 

# Construcción de la aplicación
class App:
    def __init__(self, env):
        self.app = Flask(__name__)
        self.env = env
        self.setup_infraestructure()
        #self.db = connect_db(self.env)

    def setup_infraestructure(self):
        authAdapter = AuthAdapter(self.app)
        userAdapter = UserAdapter(self.app)

# Lectura de variables de entorno
def get_env():
    with open("src/resources.yaml", "r") as f:
        return yaml.safe_load(f)