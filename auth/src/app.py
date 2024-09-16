import os
import inspect
import importlib
from src.infraestructure.adapters.auth import AuthAdapter
from src.infraestructure.adapters.user import UserAdapter
from src.root import app

# Construcción de la aplicación
class App:
    def __init__(self):
        self.app = app
        self.setup_infraestructure()

    def setup_infraestructure(self):
        authAdapter = AuthAdapter(self.app)
        userAdapter = UserAdapter(self.app)