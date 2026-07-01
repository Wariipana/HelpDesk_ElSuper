from flask import Blueprint
from flask_jwt_extended import JWTManager

from apis.api_auth import api_auth
from apis.api_usuarios import api_usuarios
from apis.api_sedes import api_sedes
from apis.api_tickets import api_tickets
from apis.api_solicitudes_cliente import api_solicitudes_cliente
from apis.api_movimientos_equipo import api_movimientos_equipo
from apis.api_trabajadores import api_trabajadores


def registrar_apis(app):
    jwt = JWTManager(app)

    app.register_blueprint(api_auth)
    app.register_blueprint(api_usuarios)
    app.register_blueprint(api_sedes)
    app.register_blueprint(api_tickets)
    app.register_blueprint(api_solicitudes_cliente)
    app.register_blueprint(api_movimientos_equipo)
    app.register_blueprint(api_trabajadores)

    return jwt
