import pymysql

from solicitudClienteClass import SolicitudCliente


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


def insertar_solicitud_cliente(objSolicitud: SolicitudCliente):
    try:
        connection = obtenerconexion()
        if connection:
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
                    cursor.execute(sql, (
                        objSolicitud.nombre_cliente,
                        objSolicitud.apellido_cliente,
                        objSolicitud.tipo_documento,
                        objSolicitud.numero_documento,
                        objSolicitud.telefono_cliente,
                        objSolicitud.email_cliente,
                        objSolicitud.tipo,
                        objSolicitud.motivo,
                        objSolicitud.sede_id,
                        objSolicitud.solicitado_por,
                    ))
                connection.commit()
            return True
        return False
    except pymysql.MySQLError as e:
        return e.args[1]


def listar_solicitudes_cliente():
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "SELECT `id`, `nombre_cliente`, `apellido_cliente`, "
                        "`tipo_documento`, `numero_documento`, "
                        "`tipo`, `sede_id` "
                        "FROM `solicitudes_cliente`"
                    )
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    return result
        return None
    except:
        return None


def obtener_solicitud_cliente_x_id(p_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "SELECT `id`, `nombre_cliente`, `apellido_cliente`, "
                        "`tipo_documento`, `numero_documento`, "
                        "`telefono_cliente`, `email_cliente`, "
                        "`tipo`, `motivo`, `sede_id`, `solicitado_por` "
                        "FROM `solicitudes_cliente` WHERE `id` = %s"
                    )
                    cursor.execute(sql, p_id)
                    result = cursor.fetchall()
                    return result
        return None
    except:
        raise


def actualizar_solicitud_cliente(objSolicitud: SolicitudCliente):
    try:
        connection = obtenerconexion()
        if connection:
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
                    cursor.execute(sql, (
                        objSolicitud.nombre_cliente,
                        objSolicitud.apellido_cliente,
                        objSolicitud.tipo_documento,
                        objSolicitud.numero_documento,
                        objSolicitud.telefono_cliente,
                        objSolicitud.email_cliente,
                        objSolicitud.tipo,
                        objSolicitud.motivo,
                        objSolicitud.sede_id,
                        objSolicitud.solicitado_por,
                        objSolicitud.id,
                    ))
                connection.commit()
            return True
        return False
    except pymysql.MySQLError as e:
        return e.args[1]


def eliminar_solicitud_cliente(p_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = "DELETE FROM `solicitudes_cliente` WHERE `id` = %s"
                    cursor.execute(sql, p_id)
                connection.commit()
            return True
        return False
    except pymysql.MySQLError as e:
        return e.args[1]
