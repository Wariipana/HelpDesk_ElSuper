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
