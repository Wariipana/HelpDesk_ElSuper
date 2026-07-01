from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from conexionBD import obtenerconexion

api_auth = Blueprint('api_auth', __name__)


@api_auth.route("/api_login", methods=['POST'])
def api_login():
    username = request.json.get("username", "")
    password = request.json.get("password", "")

    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = (
                "SELECT `id`, `nombre_completo`, `username`, `rol`, `sede_id`, `activo` "
                "FROM `usuarios` "
                "WHERE `username` = %s AND `password` = %s AND `activo` = 1"
            )
            cursor.execute(sql, (username, password))
            usuario = cursor.fetchone()

    if usuario is None:
        return jsonify({"estado": "Credenciales incorrectas"}), 401

    token = create_access_token(identity=str(usuario["id"]))
    return jsonify({"token": token, "usuario": usuario})
