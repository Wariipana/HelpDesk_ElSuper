import pymysql

from ticketClass import Ticket
from conexionBD import obtenerconexion

# -----------------------------------------------
def insertar_ticket(objTicket: Ticket):
    try:
        connection = obtenerconexion()
        if connection:
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
                    cursor.execute(sql, (
                        objTicket.titulo,
                        objTicket.descripcion,
                        objTicket.categoria,
                        objTicket.prioridad,
                        objTicket.equipo_afectado,
                        objTicket.cantidad_equipos,
                        objTicket.nombre_contacto,
                        objTicket.telefono_contacto,
                        objTicket.sede_id,
                        objTicket.creado_por,
                    ))
                connection.commit()
            return True
        return False
    except pymysql.MySQLError as e:
        return e.args[1]


def listar_tickets():
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "SELECT t.`id`, t.`titulo`, t.`categoria`, t.`prioridad`, "
                        "t.`estado`, t.`equipo_afectado`, t.`nombre_contacto`, "
                        "s.`nombre` AS `sede`, u.`username` AS `creado_por` "
                        "FROM `tickets` t "
                        "LEFT JOIN `sedes` s ON t.`sede_id` = s.`id` "
                        "LEFT JOIN `usuarios` u ON t.`creado_por` = u.`id`"
                    )
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    return result
        return None
    except:
        return None


def listar_tickets_x_sede(sede_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "SELECT t.`id`, t.`titulo`, t.`categoria`, t.`prioridad`, "
                        "t.`estado`, t.`equipo_afectado`, t.`nombre_contacto`, "
                        "s.`nombre` AS `sede`, u.`username` AS `creado_por` "
                        "FROM `tickets` t "
                        "LEFT JOIN `sedes` s ON t.`sede_id` = s.`id` "
                        "LEFT JOIN `usuarios` u ON t.`creado_por` = u.`id` "
                        "WHERE t.`sede_id` = %s"
                    )
                    cursor.execute(sql, sede_id)
                    return cursor.fetchall()
        return None
    except:
        return None


def obtener_ticket_detalle(p_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "SELECT t.`id`, t.`titulo`, t.`descripcion`, t.`categoria`, "
                        "t.`prioridad`, t.`estado`, t.`comentario_admin`, "
                        "t.`equipo_afectado`, t.`cantidad_equipos`, "
                        "t.`nombre_contacto`, t.`telefono_contacto`, "
                        "t.`fecha_limite`, t.`created_at`, t.`updated_at`, "
                        "t.`resuelto_at`, "
                        "s.`nombre` AS `sede`, "
                        "uc.`nombre_completo` AS `creado_por`, "
                        "ur.`nombre_completo` AS `resuelto_por` "
                        "FROM `tickets` t "
                        "LEFT JOIN `sedes` s ON t.`sede_id` = s.`id` "
                        "LEFT JOIN `usuarios` uc ON t.`creado_por` = uc.`id` "
                        "LEFT JOIN `usuarios` ur ON t.`resuelto_por` = ur.`id` "
                        "WHERE t.`id` = %s"
                    )
                    cursor.execute(sql, p_id)
                    return cursor.fetchone()
        return None
    except:
        raise


def gestionar_ticket(p_id, estado, comentario, resuelto_por_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    if estado == 'resuelto':
                        sql = (
                            "UPDATE `tickets` "
                            "SET `estado` = %s, `comentario_admin` = %s, "
                            "`resuelto_por` = %s, `resuelto_at` = NOW() "
                            "WHERE `id` = %s"
                        )
                        cursor.execute(sql, (estado, comentario, resuelto_por_id, p_id))
                    else:
                        sql = (
                            "UPDATE `tickets` "
                            "SET `estado` = %s, `comentario_admin` = %s "
                            "WHERE `id` = %s"
                        )
                        cursor.execute(sql, (estado, comentario, p_id))
                connection.commit()
            return True
        return False
    except pymysql.MySQLError as e:
        return e.args[1]


def obtener_ticket_x_id(p_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "SELECT `id`, `titulo`, `descripcion`, `categoria`, `prioridad`, "
                        "`equipo_afectado`, `cantidad_equipos`, "
                        "`nombre_contacto`, `telefono_contacto`, "
                        "`sede_id`, `creado_por` "
                        "FROM `tickets` WHERE `id` = %s"
                    )
                    cursor.execute(sql, p_id)
                    result = cursor.fetchall()
                    return result
        return None
    except:
        raise


def actualizar_ticket(objTicket: Ticket):
    try:
        connection = obtenerconexion()
        if connection:
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
                    cursor.execute(sql, (
                        objTicket.titulo,
                        objTicket.descripcion,
                        objTicket.categoria,
                        objTicket.prioridad,
                        objTicket.equipo_afectado,
                        objTicket.cantidad_equipos,
                        objTicket.nombre_contacto,
                        objTicket.telefono_contacto,
                        objTicket.sede_id,
                        objTicket.creado_por,
                        objTicket.id,
                    ))
                connection.commit()
            return True
        return False
    except pymysql.MySQLError as e:
        return e.args[1]


def eliminar_ticket(p_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = "DELETE FROM `tickets` WHERE `id` = %s"
                    cursor.execute(sql, p_id)
                connection.commit()
            return True
        return False
    except pymysql.MySQLError as e:
        return e.args[1]


