import pymysql

from sedeClass import Sede


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


def insertar_sede(objSede: Sede):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `sedes` (`nombre`, `direccion`) VALUES (%s, %s)"
                    cursor.execute(sql, (objSede.nombre, objSede.direccion))
                connection.commit()
            return True
        return False
    except pymysql.MySQLError as e:
        return e.args[1]
