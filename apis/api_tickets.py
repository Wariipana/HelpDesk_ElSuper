from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from conexionBD import obtenerconexion

api_tickets = Blueprint('api_tickets', __name__)


@api_tickets.route("/api_leertickets")
@jwt_required()
def api_leertickets():
    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = (
                "SELECT t.`id`, t.`titulo`, t.`descripcion`, t.`categoria`, t.`prioridad`, "
                "t.`estado`, t.`equipo_afectado`, t.`cantidad_equipos`, "
                "t.`nombre_contacto`, t.`telefono_contacto`, "
                "t.`sede_id`, s.`nombre` AS `sede`, "
                "t.`creado_por`, u.`username` AS `creado_por_username`, "
                "t.`created_at` "
                "FROM `tickets` t "
                "LEFT JOIN `sedes` s ON t.`sede_id` = s.`id` "
                "LEFT JOIN `usuarios` u ON t.`creado_por` = u.`id`"
            )
            cursor.execute(sql)
            result = cursor.fetchall()
    return jsonify(result)


@api_tickets.route("/api_leerticketxid/<int:id>")
@jwt_required()
def api_leerticketxid(id):
    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = (
                "SELECT t.`id`, t.`titulo`, t.`descripcion`, t.`categoria`, t.`prioridad`, "
                "t.`estado`, t.`comentario_admin`, t.`equipo_afectado`, t.`cantidad_equipos`, "
                "t.`nombre_contacto`, t.`telefono_contacto`, "
                "t.`sede_id`, s.`nombre` AS `sede`, "
                "t.`creado_por`, u.`username` AS `creado_por_username`, "
                "t.`created_at`, t.`updated_at`, t.`resuelto_at` "
                "FROM `tickets` t "
                "LEFT JOIN `sedes` s ON t.`sede_id` = s.`id` "
                "LEFT JOIN `usuarios` u ON t.`creado_por` = u.`id` "
                "WHERE t.`id` = %s"
            )
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
    if result is None:
        return jsonify({"estado": "Ticket no encontrado"}), 404
    return jsonify(result)


@api_tickets.route("/api_guardarticket", methods=['POST'])
@jwt_required()
def api_guardarticket():
    titulo             = request.json["titulo"]
    descripcion        = request.json["descripcion"]
    categoria          = request.json["categoria"]
    prioridad          = request.json["prioridad"]
    equipo_afectado    = request.json["equipo_afectado"]
    cantidad_equipos   = request.json["cantidad_equipos"]
    nombre_contacto    = request.json["nombre_contacto"]
    telefono_contacto  = request.json["telefono_contacto"]
    sede_id            = request.json["sede_id"]
    creado_por         = request.json["creado_por"]

    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = (
                "INSERT INTO `tickets` "
                "(`titulo`, `descripcion`, `categoria`, `prioridad`, "
                "`equipo_afectado`, `cantidad_equipos`, "
                "`nombre_contacto`, `telefono_contacto`, "
                "`sede_id`, `creado_por`) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )
            cursor.execute(sql, (titulo, descripcion, categoria, prioridad,
                                 equipo_afectado, cantidad_equipos,
                                 nombre_contacto, telefono_contacto,
                                 sede_id, creado_por))
        connection.commit()
    return jsonify({"estado": "Insercion correcta"})


@api_tickets.route("/api_actualizarticket", methods=['PUT'])
@jwt_required()
def api_actualizarticket():
    id                 = request.json["id"]
    titulo             = request.json["titulo"]
    descripcion        = request.json["descripcion"]
    categoria          = request.json["categoria"]
    prioridad          = request.json["prioridad"]
    equipo_afectado    = request.json["equipo_afectado"]
    cantidad_equipos   = request.json["cantidad_equipos"]
    nombre_contacto    = request.json["nombre_contacto"]
    telefono_contacto  = request.json["telefono_contacto"]
    sede_id            = request.json["sede_id"]
    creado_por         = request.json["creado_por"]

    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = (
                "UPDATE `tickets` "
                "SET `titulo` = %s, `descripcion` = %s, `categoria` = %s, "
                "`prioridad` = %s, `equipo_afectado` = %s, `cantidad_equipos` = %s, "
                "`nombre_contacto` = %s, `telefono_contacto` = %s, "
                "`sede_id` = %s, `creado_por` = %s "
                "WHERE `id` = %s"
            )
            cursor.execute(sql, (titulo, descripcion, categoria, prioridad,
                                 equipo_afectado, cantidad_equipos,
                                 nombre_contacto, telefono_contacto,
                                 sede_id, creado_por, id))
        connection.commit()
    return jsonify({"estado": "Actualizacion correcta"})


@api_tickets.route("/api_eliminarticket/<int:id>", methods=['DELETE'])
@jwt_required()
def api_eliminarticket(id):
    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = "DELETE FROM `tickets` WHERE `id` = %s"
            cursor.execute(sql, (id,))
        connection.commit()
    return jsonify({"estado": "Eliminacion correcta"})
