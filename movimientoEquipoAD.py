import pymysql

from movimientoEquipoClass import MovimientoEquipo
from conexionBD import obtenerconexion


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
                        "SELECT me.`id`, me.`tipo`, me.`tipo_equipo`, me.`modelo`, "
                        "me.`numero_serie`, s.`nombre` AS `sede`, me.`responsable`, "
                        "me.`fecha`, u.`username` AS `registrado_por` "
                        "FROM `movimientos_equipo` me "
                        "LEFT JOIN `sedes` s ON me.`sede_id` = s.`id` "
                        "LEFT JOIN `usuarios` u ON me.`registrado_por` = u.`id`"
                    )
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    return result
        return None
    except:
        return None


def listar_movimientos_filtrado(fecha_desde=None, fecha_hasta=None,
                                sede_id=None, tipo=None, tipo_equipo=None,
                                pagina=1, por_pagina=20):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    base = (
                        "SELECT me.`id`, me.`tipo`, me.`tipo_equipo`, me.`modelo`, "
                        "me.`numero_serie`, s.`nombre` AS `sede`, me.`responsable`, "
                        "me.`fecha`, u.`username` AS `registrado_por` "
                        "FROM `movimientos_equipo` me "
                        "LEFT JOIN `sedes` s ON me.`sede_id` = s.`id` "
                        "LEFT JOIN `usuarios` u ON me.`registrado_por` = u.`id` "
                        "WHERE 1=1 "
                    )
                    params = []

                    if fecha_desde:
                        base += "AND me.`fecha` >= %s "
                        params.append(fecha_desde)
                    if fecha_hasta:
                        base += "AND me.`fecha` <= %s "
                        params.append(fecha_hasta)
                    if sede_id:
                        base += "AND me.`sede_id` = %s "
                        params.append(sede_id)
                    if tipo:
                        base += "AND me.`tipo` = %s "
                        params.append(tipo)
                    if tipo_equipo:
                        base += "AND me.`tipo_equipo` LIKE %s "
                        params.append('%' + tipo_equipo + '%')

                    count_sql = "SELECT COUNT(*) AS total FROM (" + base + ") sub"
                    cursor.execute(count_sql, params)
                    total = cursor.fetchone()['total']

                    offset = (pagina - 1) * por_pagina
                    base += "ORDER BY me.`fecha` DESC LIMIT %s OFFSET %s"
                    params.append(por_pagina)
                    params.append(offset)

                    cursor.execute(base, params)
                    registros = cursor.fetchall()
                    return registros, total
        return [], 0
    except:
        return [], 0


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
