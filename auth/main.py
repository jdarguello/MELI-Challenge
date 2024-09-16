from src.app import *

# Inicio y gestión del microservicio
if __name__ == "__main__":
    env = get_env()
    create_app().run(debug=env["main"]["debug"])