from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from conexionBD import obtenerconexion

api_sedes = Blueprint('api_sedes', __name__)


@api_sedes.route("/api_leersedes")
@jwt_required()
def api_leersedes():
    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT `id`, `nombre`, `direccion` FROM `sedes`"
            cursor.execute(sql)
            result = cursor.fetchall()
    return jsonify(result)


@api_sedes.route("/api_leersedexid/<int:id>")
@jwt_required()
def api_leersedexid(id):
    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT `id`, `nombre`, `direccion` FROM `sedes` WHERE `id` = %s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
    if result is None:
        return jsonify({"estado": "Sede no encontrada"}), 404
    return jsonify(result)


@api_sedes.route("/api_guardarsede", methods=['POST'])
@jwt_required()
def api_guardarsede():
    nombre    = request.json["nombre"]
    direccion = request.json["direccion"]

    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `sedes` (`nombre`, `direccion`) VALUES (%s, %s)"
            cursor.execute(sql, (nombre, direccion))
        connection.commit()
    return jsonify({"estado": "Insercion correcta"})


@api_sedes.route("/api_actualizarsede", methods=['PUT'])
@jwt_required()
def api_actualizarsede():
    id        = request.json["id"]
    nombre    = request.json["nombre"]
    direccion = request.json["direccion"]

    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = (
                "UPDATE `sedes` "
                "SET `nombre` = %s, `direccion` = %s "
                "WHERE `id` = %s"
            )
            cursor.execute(sql, (nombre, direccion, id))
        connection.commit()
    return jsonify({"estado": "Actualizacion correcta"})


@api_sedes.route("/api_eliminarsede/<int:id>", methods=['DELETE'])
@jwt_required()
def api_eliminarsede(id):
    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = "DELETE FROM `sedes` WHERE `id` = %s"
            cursor.execute(sql, (id,))
        connection.commit()
    return jsonify({"estado": "Eliminacion correcta"})
