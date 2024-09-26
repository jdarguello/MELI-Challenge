---
sidebar_position: 5
---

# CORS

El mecanismo de _Cross-Origin Resource Sharing_ (CORS) busca garantizar la confiabilidad durante la comunicación entre distintos componentes de software, principalmente sobre aquellos procedentes de la web. 

![](../../../static/img/sdlc/seguridad/cors.png)

Figura. Funcionamiento de CORS.

En Flask, existe la librería `flask_cors`, con la que se puede incrementar la confiabilidad sobre el origen de las peticiones. 

```py
from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/data', methods=['GET'])
@cross_origin(origins=["https://your-frontend.com"])
def data():
    return {"message": "This is a CORS-enabled response"}
```