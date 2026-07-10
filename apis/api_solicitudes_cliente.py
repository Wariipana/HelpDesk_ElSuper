from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required
from conexionBD import obtenerconexion

api_solicitudes_cliente = Blueprint('api_solicitudes_cliente', __name__)


@api_solicitudes_cliente.route("/api_leersolicitudescliente")
@jwt_required()
def api_leersolicitudescliente():
    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = (
                "SELECT sc.`id`, sc.`nombre_cliente`, sc.`apellido_cliente`, "
                "sc.`tipo_documento`, sc.`numero_documento`, "
                "sc.`telefono_cliente`, sc.`email_cliente`, "
                "sc.`tipo`, sc.`motivo`, sc.`estado`, "
                "sc.`sede_id`, s.`nombre` AS `sede`, "
                "sc.`solicitado_por`, u.`username` AS `solicitado_por_username`, "
                "sc.`created_at` "
                "FROM `solicitudes_cliente` sc "
                "LEFT JOIN `sedes` s ON sc.`sede_id` = s.`id` "
                "LEFT JOIN `usuarios` u ON sc.`solicitado_por` = u.`id`"
            )
            cursor.execute(sql)
            result = cursor.fetchall()
    return jsonify(result)


@api_solicitudes_cliente.route("/api_leersolicitudclientexid/<int:id>")
@jwt_required()
def api_leersolicitudclientexid(id):
    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = (
                "SELECT sc.`id`, sc.`nombre_cliente`, sc.`apellido_cliente`, "
                "sc.`tipo_documento`, sc.`numero_documento`, "
                "sc.`telefono_cliente`, sc.`email_cliente`, "
                "sc.`tipo`, sc.`motivo`, sc.`estado`, sc.`observacion_admin`, "
                "sc.`sede_id`, s.`nombre` AS `sede`, "
                "sc.`solicitado_por`, u.`username` AS `solicitado_por_username`, "
                "sc.`created_at`, sc.`updated_at`, sc.`resuelto_at` "
                "FROM `solicitudes_cliente` sc "
                "LEFT JOIN `sedes` s ON sc.`sede_id` = s.`id` "
                "LEFT JOIN `usuarios` u ON sc.`solicitado_por` = u.`id` "
                "WHERE sc.`id` = %s"
            )
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
    if result is None:
        return jsonify({"estado": "Solicitud no encontrada"}), 404
    return jsonify(result)


@api_solicitudes_cliente.route("/api_guardarsolicitudcliente", methods=['POST'])
@jwt_required()
def api_guardarsolicitudcliente():
    nombre_cliente    = request.json["nombre_cliente"]
    apellido_cliente  = request.json["apellido_cliente"]
    tipo_documento    = request.json["tipo_documento"]
    numero_documento  = request.json["numero_documento"]
    telefono_cliente  = request.json["telefono_cliente"]
    email_cliente     = request.json["email_cliente"]
    tipo              = request.json["tipo"]
    motivo            = request.json["motivo"]
    sede_id           = request.json["sede_id"]
    solicitado_por    = request.json["solicitado_por"]

    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = (
                "INSERT INTO `solicitudes_cliente` "
                "(`nombre_cliente`, `apellido_cliente`, "
                "`tipo_documento`, `numero_documento`, "
                "`telefono_cliente`, `email_cliente`, "
                "`tipo`, `motivo`, `sede_id`, `solicitado_por`) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )
            cursor.execute(sql, (nombre_cliente, apellido_cliente,
                                 tipo_documento, numero_documento,
                                 telefono_cliente, email_cliente,
                                 tipo, motivo, sede_id, solicitado_por))
        connection.commit()
    return jsonify({"estado": "Insercion correcta"})


@api_solicitudes_cliente.route("/api_actualizarsolicitudcliente", methods=['PUT'])
@jwt_required()
def api_actualizarsolicitudcliente():
    id                = request.json["id"]
    nombre_cliente    = request.json["nombre_cliente"]
    apellido_cliente  = request.json["apellido_cliente"]
    tipo_documento    = request.json["tipo_documento"]
    numero_documento  = request.json["numero_documento"]
    telefono_cliente  = request.json["telefono_cliente"]
    email_cliente     = request.json["email_cliente"]
    tipo              = request.json["tipo"]
    motivo            = request.json["motivo"]
    sede_id           = request.json["sede_id"]
    solicitado_por    = request.json["solicitado_por"]

    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = (
                "UPDATE `solicitudes_cliente` "
                "SET `nombre_cliente` = %s, `apellido_cliente` = %s, "
                "`tipo_documento` = %s, `numero_documento` = %s, "
                "`telefono_cliente` = %s, `email_cliente` = %s, "
                "`tipo` = %s, `motivo` = %s, `sede_id` = %s, `solicitado_por` = %s "
                "WHERE `id` = %s"
            )
            cursor.execute(sql, (nombre_cliente, apellido_cliente,
                                 tipo_documento, numero_documento,
                                 telefono_cliente, email_cliente,
                                 tipo, motivo, sede_id, solicitado_por, id))
        connection.commit()
    return jsonify({"estado": "Actualizacion correcta"})


@api_solicitudes_cliente.route("/api_eliminarsolicitudcliente/<int:id>", methods=['DELETE'])
@jwt_required()
def api_eliminarsolicitudcliente(id):
    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = "DELETE FROM `solicitudes_cliente` WHERE `id` = %s"
            cursor.execute(sql, (id,))
        connection.commit()
    return jsonify({"estado": "Eliminacion correcta"})
