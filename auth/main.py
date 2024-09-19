from src.app import App
from src.root import get_env_vars

# Inicio y gestión del microservicio
if __name__ == "__main__":
    env = get_env_vars()
    application = App()
    application.app.run(debug=env["debug"])