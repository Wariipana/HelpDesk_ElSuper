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
                        "SELECT `id`, `tipo`, `tipo_equipo`, `modelo`, "
                        "`numero_serie`, `sede_id`, `responsable`, `fecha` "
                        "FROM `movimientos_equipo`"
                    )
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    return result
        return None
    except:
        return None


def obtener_movimiento_equipo_x_id(p_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "SELECT `id`, `tipo`, `tipo_equipo`, `modelo`, `numero_serie`, "
                        "`sede_id`, `responsable`, `fecha`, `registrado_por` "
                        "FROM `movimientos_equipo` WHERE `id` = %s"
                    )
                    cursor.execute(sql, p_id)
                    result = cursor.fetchall()
                    return result
        return None
    except:
        raise


def actualizar_movimiento_equipo(objMovimiento: MovimientoEquipo):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "UPDATE `movimientos_equipo` "
                        "SET `tipo` = %s, `tipo_equipo` = %s, `modelo` = %s, `numero_serie` = %s, "
                        "`sede_id` = %s, `responsable` = %s, `fecha` = %s, `registrado_por` = %s "
                        "WHERE `id` = %s"
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
                        objMovimiento.id,
                    ))
                connection.commit()
            return True
        return False
    except pymysql.MySQLError as e:
        return e.args[1]


def eliminar_movimiento_equipo(p_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = "DELETE FROM `movimientos_equipo` WHERE `id` = %s"
                    cursor.execute(sql, p_id)
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
                        "SELECT `id`, `tipo`, `tipo_equipo`, `modelo`, "
                        "`numero_serie`, `sede_id`, `responsable`, `fecha` "
                        "FROM `movimientos_equipo`"
                    )
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    return result
        return None
    except:
        return None


def obtener_movimiento_equipo_x_id(p_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "SELECT `id`, `tipo`, `tipo_equipo`, `modelo`, `numero_serie`, "
                        "`sede_id`, `responsable`, `fecha`, `registrado_por` "
                        "FROM `movimientos_equipo` WHERE `id` = %s"
                    )
                    cursor.execute(sql, p_id)
                    result = cursor.fetchall()
                    return result
        return None
    except:
        raise


def actualizar_movimiento_equipo(objMovimiento: MovimientoEquipo):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "UPDATE `movimientos_equipo` "
                        "SET `tipo` = %s, `tipo_equipo` = %s, `modelo` = %s, `numero_serie` = %s, "
                        "`sede_id` = %s, `responsable` = %s, `fecha` = %s, `registrado_por` = %s "
                        "WHERE `id` = %s"
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
                        objMovimiento.id,
                    ))
                connection.commit()
            return True
        return False
    except pymysql.MySQLError as e:
        return e.args[1]


def eliminar_movimiento_equipo(p_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = "DELETE FROM `movimientos_equipo` WHERE `id` = %s"
                    cursor.execute(sql, p_id)
                connection.commit()
            return True
        return False
    except pymysql.MySQLError as e:
        return e.args[1]
