from src.app import *

environment = "tests"

# Inicio y gestión del microservicio
if __name__ == "__main__":
    env = get_env()[environment]
    application = App(env)
    application.app.run(debug=env["debug"])