import pymysql

from ticketClass import Ticket


def obtenerconexion():
    try:
        connection = pymysql.connect(
            host='trolley.proxy.rlwy.net',
            port=23707,
            user='root',
            password='hkgInrsJKwLolWdhqHOnoPtLGIpQpVMe',
            database='railway',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        return None


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
