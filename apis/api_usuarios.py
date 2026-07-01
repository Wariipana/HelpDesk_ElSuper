from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from conexionBD import obtenerconexion

api_usuarios = Blueprint('api_usuarios', __name__)


@api_usuarios.route("/api_leerusuarios")
@jwt_required()
def api_leerusuarios():
    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = (
                "SELECT u.`id`, u.`nombre_completo`, u.`username`, u.`rol`, "
                "u.`sede_id`, s.`nombre` AS `sede`, u.`activo` "
                "FROM `usuarios` u "
                "LEFT JOIN `sedes` s ON u.`sede_id` = s.`id`"
            )
            cursor.execute(sql)
            result = cursor.fetchall()
    return jsonify(result)


@api_usuarios.route("/api_leerusuarioxid/<int:id>")
@jwt_required()
def api_leerusuarioxid(id):
    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = (
                "SELECT u.`id`, u.`nombre_completo`, u.`username`, u.`rol`, "
                "u.`sede_id`, s.`nombre` AS `sede`, u.`activo` "
                "FROM `usuarios` u "
                "LEFT JOIN `sedes` s ON u.`sede_id` = s.`id` "
                "WHERE u.`id` = %s"
            )
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
    if result is None:
        return jsonify({"estado": "Usuario no encontrado"}), 404
    return jsonify(result)


@api_usuarios.route("/api_guardarusuario", methods=['POST'])
@jwt_required()
def api_guardarusuario():
    nombre_completo = request.json["nombre_completo"]
    username        = request.json["username"]
    password        = request.json["password"]
    rol             = request.json["rol"]
    sede_id         = request.json["sede_id"]
    activo          = request.json["activo"]

    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = (
                "INSERT INTO `usuarios` "
                "(`nombre_completo`, `username`, `password`, `rol`, `sede_id`, `activo`) "
                "VALUES (%s, %s, %s, %s, %s, %s)"
            )
            cursor.execute(sql, (nombre_completo, username, password, rol, sede_id, activo))
        connection.commit()
    return jsonify({"estado": "Insercion correcta"})


@api_usuarios.route("/api_actualizarusuario", methods=['PUT'])
@jwt_required()
def api_actualizarusuario():
    id              = request.json["id"]
    nombre_completo = request.json["nombre_completo"]
    username        = request.json["username"]
    password        = request.json["password"]
    rol             = request.json["rol"]
    sede_id         = request.json["sede_id"]
    activo          = request.json["activo"]

    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = (
                "UPDATE `usuarios` "
                "SET `nombre_completo` = %s, `username` = %s, `password` = %s, "
                "`rol` = %s, `sede_id` = %s, `activo` = %s "
                "WHERE `id` = %s"
            )
            cursor.execute(sql, (nombre_completo, username, password, rol, sede_id, activo, id))
        connection.commit()
    return jsonify({"estado": "Actualizacion correcta"})


@api_usuarios.route("/api_eliminarusuario/<int:id>", methods=['DELETE'])
@jwt_required()
def api_eliminarusuario(id):
    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = "DELETE FROM `usuarios` WHERE `id` = %s"
            cursor.execute(sql, (id,))
        connection.commit()
    return jsonify({"estado": "Eliminacion correcta"})
