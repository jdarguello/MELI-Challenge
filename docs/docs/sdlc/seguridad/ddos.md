---
sidebar_position: 3
---

# DDoS

Los ataques por DDoS buscan vulnerar la capacidad de infraestructura y generar indisponibilidad en los servicios. Es posible mitigar estos ataques a nivel de API Gateway. Sin embargo, también es posible ejecutar consideraciones en el diseño de software que ayuden a mitigar este tipo de vulneración del sistema.

En Flask, se puede implementar la librería `flask_limiter`, que ayuda a limitar la cantidad máxima de TPS que se pueden procesar en el tiempo, como se muestra a continuación.

```py
from flask import Flask
from flask_limiter import Limiter

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)

@app.route("/api")
@limiter.limit("10 per minute")
def api():
    return "This is rate-limited!"

```

Sin embargo, tomar esa decisión requiere un estudio minucioso de la aplicación y de cuántos usuarios se esperaría recibir peticiones de manera legítima.
