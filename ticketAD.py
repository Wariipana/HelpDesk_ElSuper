import pymysql

from ticketClass import Ticket
from conexionBD import obtenerconexion


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
                        "SELECT `id`, `titulo`, `categoria`, `prioridad`, "
                        "`equipo_afectado`, `nombre_contacto`, `sede_id` "
                        "FROM `tickets`"
                    )
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    return result
        return None
    except:
        return None


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


