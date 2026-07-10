import pymysql


def obtenerconexion():
    try:
        connection = pymysql.connect(
            host='trolley.proxy.rlwy.net',
            port=23707,
            user='root',
            password='hkgInrsJKwLolWdhqHOnoPtLGIpQpVMe',
            database='railway',
            cursorclass=pymysql.cursors.DictCursor,
            # Peru no usa horario de verano, por eso el offset fijo -05:00
            # (evita depender de las tablas de zonas horarias del servidor MySQL).
            init_command="SET time_zone = '-05:00'"
        )
        return connection
    except pymysql.MySQLError as e:
        return None
