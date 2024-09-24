from src.app import App
from src.root import get_env_vars

# Inicio y gestión del microservicio
if __name__ == "__main__":
    env = get_env_vars()
    application = App()
    #application.flask_app.run(debug=env["debug"])
    application.flask_app.run(host="0.0.0.0", port=5000, debug=env["debug"])