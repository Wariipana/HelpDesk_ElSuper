from flask_jwt import JWT

from apis.api_auth import authenticate, identity
from apis.api_usuarios import api_usuarios
from apis.api_sedes import api_sedes
from apis.api_tickets import api_tickets
from apis.api_solicitudes_cliente import api_solicitudes_cliente
from apis.api_movimientos_equipo import api_movimientos_equipo
from apis.api_trabajadores import api_trabajadores


def registrar_apis(app):
    # Registra el endpoint de login por defecto de flask-jwt (POST /auth)
    # usando authenticate()/identity() de apis/api_auth.py.
    jwt = JWT(app, authenticate, identity)

    app.register_blueprint(api_usuarios)
    app.register_blueprint(api_sedes)
    app.register_blueprint(api_tickets)
    app.register_blueprint(api_solicitudes_cliente)
    app.register_blueprint(api_movimientos_equipo)
    app.register_blueprint(api_trabajadores)

    return jwt
