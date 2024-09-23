import os
import inspect
import importlib
from src.infraestructure.adapters.inbound.auth import auth_bp
from src.infraestructure.adapters.inbound.admin import admin_bp
from src.root import app

# Construcción de la aplicación
class App:
    have_instance = False
    def __init__(self):
        self.flask_app = app
        self.setup_infraestructure()

    def setup_infraestructure(self):
        self.flask_app.register_blueprint(auth_bp)
        self.flask_app.register_blueprint(admin_bp)