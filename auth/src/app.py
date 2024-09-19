import os
import inspect
import importlib
from src.infraestructure.adapters.auth import AuthAdapter
from src.infraestructure.adapters.user import UserAdapter
from src.root import app

# Construcción de la aplicación
class App:
    def __init__(self):
        self.flask_app = app
        self.setup_infraestructure()

    def setup_infraestructure(self):
        AuthAdapter(self.flask_app)
        UserAdapter(self.flask_app)