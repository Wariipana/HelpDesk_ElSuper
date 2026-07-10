from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required
from conexionBD import obtenerconexion

api_movimientos_equipo = Blueprint('api_movimientos_equipo', __name__)


@api_movimientos_equipo.route("/api_leermovimientosequipo")
@jwt_required()
def api_leermovimientosequipo():
    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = (
                "SELECT me.`id`, me.`tipo`, me.`tipo_equipo`, me.`modelo`, "
                "me.`numero_serie`, me.`sede_id`, s.`nombre` AS `sede`, "
                "me.`responsable`, me.`fecha`, "
                "me.`registrado_por`, u.`username` AS `registrado_por_username` "
                "FROM `movimientos_equipo` me "
                "LEFT JOIN `sedes` s ON me.`sede_id` = s.`id` "
                "LEFT JOIN `usuarios` u ON me.`registrado_por` = u.`id`"
            )
            cursor.execute(sql)
            result = cursor.fetchall()
    return jsonify(result)


@api_movimientos_equipo.route("/api_leermovimientoequipoxid/<int:id>")
@jwt_required()
def api_leermovimientoequipoxid(id):
    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = (
                "SELECT me.`id`, me.`tipo`, me.`tipo_equipo`, me.`modelo`, "
                "me.`numero_serie`, me.`sede_id`, s.`nombre` AS `sede`, "
                "me.`responsable`, me.`fecha`, "
                "me.`registrado_por`, u.`username` AS `registrado_por_username` "
                "FROM `movimientos_equipo` me "
                "LEFT JOIN `sedes` s ON me.`sede_id` = s.`id` "
                "LEFT JOIN `usuarios` u ON me.`registrado_por` = u.`id` "
                "WHERE me.`id` = %s"
            )
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
    if result is None:
        return jsonify({"estado": "Movimiento no encontrado"}), 404
    return jsonify(result)


@api_movimientos_equipo.route("/api_guardarmovimientoequipo", methods=['POST'])
@jwt_required()
def api_guardarmovimientoequipo():
    tipo            = request.json["tipo"]
    tipo_equipo     = request.json["tipo_equipo"]
    modelo          = request.json["modelo"]
    numero_serie    = request.json["numero_serie"]
    sede_id         = request.json["sede_id"]
    responsable     = request.json["responsable"]
    fecha           = request.json["fecha"]
    registrado_por  = request.json["registrado_por"]

    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = (
                "INSERT INTO `movimientos_equipo` "
                "(`tipo`, `tipo_equipo`, `modelo`, `numero_serie`, "
                "`sede_id`, `responsable`, `fecha`, `registrado_por`) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            )
            cursor.execute(sql, (tipo, tipo_equipo, modelo, numero_serie,
                                 sede_id, responsable, fecha, registrado_por))
        connection.commit()
    return jsonify({"estado": "Insercion correcta"})


@api_movimientos_equipo.route("/api_actualizarmovimientoequipo", methods=['PUT'])
@jwt_required()
def api_actualizarmovimientoequipo():
    id              = request.json["id"]
    tipo            = request.json["tipo"]
    tipo_equipo     = request.json["tipo_equipo"]
    modelo          = request.json["modelo"]
    numero_serie    = request.json["numero_serie"]
    sede_id         = request.json["sede_id"]
    responsable     = request.json["responsable"]
    fecha           = request.json["fecha"]
    registrado_por  = request.json["registrado_por"]

    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = (
                "UPDATE `movimientos_equipo` "
                "SET `tipo` = %s, `tipo_equipo` = %s, `modelo` = %s, `numero_serie` = %s, "
                "`sede_id` = %s, `responsable` = %s, `fecha` = %s, `registrado_por` = %s "
                "WHERE `id` = %s"
            )
            cursor.execute(sql, (tipo, tipo_equipo, modelo, numero_serie,
                                 sede_id, responsable, fecha, registrado_por, id))
        connection.commit()
    return jsonify({"estado": "Actualizacion correcta"})


@api_movimientos_equipo.route("/api_eliminarmovimientoequipo/<int:id>", methods=['DELETE'])
@jwt_required()
def api_eliminarmovimientoequipo(id):
    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = "DELETE FROM `movimientos_equipo` WHERE `id` = %s"
            cursor.execute(sql, (id,))
        connection.commit()
    return jsonify({"estado": "Eliminacion correcta"})
