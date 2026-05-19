import pymysql

from movimientoEquipoClass import MovimientoEquipo


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


def insertar_movimiento_equipo(objMovimiento: MovimientoEquipo):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "INSERT INTO `movimientos_equipo` "
                        "(`tipo`, `tipo_equipo`, `modelo`, `numero_serie`, "
                        "`sede_id`, `responsable`, `fecha`, `registrado_por`) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    )
                    cursor.execute(sql, (
                        objMovimiento.tipo,
                        objMovimiento.tipo_equipo,
                        objMovimiento.modelo,
                        objMovimiento.numero_serie,
                        objMovimiento.sede_id,
                        objMovimiento.responsable,
                        objMovimiento.fecha,
                        objMovimiento.registrado_por,
                    ))
                connection.commit()
            return True
        return False
    except pymysql.MySQLError as e:
        return e.args[1]


def listar_movimientos_equipo():
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "SELECT `tipo`, `tipo_equipo`, `modelo`, "
                        "`numero_serie`, `sede_id`, `responsable`, `fecha` "
                        "FROM `movimientos_equipo`"
                    )
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    return result
        return None
    except:
        return None
