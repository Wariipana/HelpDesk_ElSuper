from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required
from conexionBD import obtenerconexion

api_trabajadores = Blueprint('api_trabajadores', __name__)


ESTADO_ROL_CASE = (
    "CASE "
    "WHEN t.`fecha_fin` IS NULL THEN 'sin_fecha_fin' "
    "WHEN t.`fecha_fin` < CURDATE() THEN 'vencido' "
    "ELSE 'vigente' END"
)


@api_trabajadores.route("/api_leertrabajadores")
@jwt_required()
def api_leertrabajadores():
    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = (
                "SELECT t.`id`, t.`nombre`, t.`apellido`, "
                "t.`tipo_documento`, t.`numero_documento`, "
                "t.`telefono`, t.`rol`, "
                "t.`fecha_inicio`, t.`fecha_fin`, "
                + ESTADO_ROL_CASE + " AS `estado_rol`, "
                "t.`sede_id`, s.`nombre` AS `sede`, "
                "t.`registrado_por`, u.`username` AS `registrado_por_username`, "
                "t.`created_at` "
                "FROM `trabajadores` t "
                "LEFT JOIN `sedes` s ON t.`sede_id` = s.`id` "
                "LEFT JOIN `usuarios` u ON t.`registrado_por` = u.`id`"
            )
            cursor.execute(sql)
            result = cursor.fetchall()
    return jsonify(result)


@api_trabajadores.route("/api_leertrabajadorxid/<int:id>")
@jwt_required()
def api_leertrabajadorxid(id):
    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = (
                "SELECT t.`id`, t.`nombre`, t.`apellido`, "
                "t.`tipo_documento`, t.`numero_documento`, "
                "t.`telefono`, t.`rol`, "
                "t.`fecha_inicio`, t.`fecha_fin`, "
                + ESTADO_ROL_CASE + " AS `estado_rol`, "
                "t.`sede_id`, s.`nombre` AS `sede`, "
                "t.`registrado_por`, u.`username` AS `registrado_por_username`, "
                "t.`created_at`, t.`updated_at` "
                "FROM `trabajadores` t "
                "LEFT JOIN `sedes` s ON t.`sede_id` = s.`id` "
                "LEFT JOIN `usuarios` u ON t.`registrado_por` = u.`id` "
                "WHERE t.`id` = %s"
            )
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
    if result is None:
        return jsonify({"estado": "Trabajador no encontrado"}), 404
    return jsonify(result)


@api_trabajadores.route("/api_guardartrabajador", methods=['POST'])
@jwt_required()
def api_guardartrabajador():
    nombre           = request.json["nombre"]
    apellido         = request.json["apellido"]
    tipo_documento   = request.json["tipo_documento"]
    numero_documento = request.json["numero_documento"]
    telefono         = request.json.get("telefono")
    rol              = request.json["rol"]
    fecha_inicio     = request.json["fecha_inicio"]
    fecha_fin        = request.json.get("fecha_fin")
    sede_id          = request.json["sede_id"]
    registrado_por   = request.json["registrado_por"]

    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = (
                "INSERT INTO `trabajadores` "
                "(`nombre`, `apellido`, "
                "`tipo_documento`, `numero_documento`, "
                "`telefono`, `rol`, "
                "`fecha_inicio`, `fecha_fin`, "
                "`sede_id`, `registrado_por`) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )
            cursor.execute(sql, (nombre, apellido,
                                 tipo_documento, numero_documento,
                                 telefono, rol,
                                 fecha_inicio, fecha_fin,
                                 sede_id, registrado_por))
        connection.commit()
    return jsonify({"estado": "Insercion correcta"})


@api_trabajadores.route("/api_actualizartrabajador", methods=['PUT'])
@jwt_required()
def api_actualizartrabajador():
    id               = request.json["id"]
    nombre           = request.json["nombre"]
    apellido         = request.json["apellido"]
    tipo_documento   = request.json["tipo_documento"]
    numero_documento = request.json["numero_documento"]
    telefono         = request.json.get("telefono")
    rol              = request.json["rol"]
    fecha_inicio     = request.json["fecha_inicio"]
    fecha_fin        = request.json.get("fecha_fin")
    sede_id          = request.json["sede_id"]
    registrado_por   = request.json["registrado_por"]

    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = (
                "UPDATE `trabajadores` "
                "SET `nombre` = %s, `apellido` = %s, "
                "`tipo_documento` = %s, `numero_documento` = %s, "
                "`telefono` = %s, `rol` = %s, "
                "`fecha_inicio` = %s, `fecha_fin` = %s, "
                "`sede_id` = %s, `registrado_por` = %s "
                "WHERE `id` = %s"
            )
            cursor.execute(sql, (nombre, apellido,
                                 tipo_documento, numero_documento,
                                 telefono, rol,
                                 fecha_inicio, fecha_fin,
                                 sede_id, registrado_por, id))
        connection.commit()
    return jsonify({"estado": "Actualizacion correcta"})


@api_trabajadores.route("/api_eliminartrabajador/<int:id>", methods=['DELETE'])
@jwt_required()
def api_eliminartrabajador(id):
    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = "DELETE FROM `trabajadores` WHERE `id` = %s"
            cursor.execute(sql, (id,))
        connection.commit()
    return jsonify({"estado": "Eliminacion correcta"})
