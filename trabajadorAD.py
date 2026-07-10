import pymysql

from trabajadorClass import Trabajador
from conexionBD import obtenerconexion


# Expresion reutilizable: estado del rol calculado a partir de fecha_fin.
#   sin_fecha_fin -> rol indefinido (sin limite)
#   vencido       -> fecha_fin ya paso (excedio el limite)
#   vigente       -> dentro del plazo
ESTADO_ROL_CASE = (
    "CASE "
    "WHEN t.`fecha_fin` IS NULL THEN 'sin_fecha_fin' "
    "WHEN t.`fecha_fin` < CURDATE() THEN 'vencido' "
    "ELSE 'vigente' END"
)


def _condicion_estado(estado):
    if estado == 'sin_fecha_fin':
        return "t.`fecha_fin` IS NULL"
    if estado == 'vencido':
        return "t.`fecha_fin` IS NOT NULL AND t.`fecha_fin` < CURDATE()"
    if estado == 'vigente':
        return "t.`fecha_fin` IS NOT NULL AND t.`fecha_fin` >= CURDATE()"
    return None


def insertar_trabajador(objTrabajador: Trabajador):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "INSERT INTO `trabajadores` "
                        "(`nombre`, `apellido`, "
                        "`tipo_documento`, `numero_documento`, "
                        "`telefono`, `rol`, "
                        "`fecha_inicio`, `fecha_fin`, "
                        "`sede_id`, `registrado_por`) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    )
                    cursor.execute(sql, (
                        objTrabajador.nombre,
                        objTrabajador.apellido,
                        objTrabajador.tipo_documento,
                        objTrabajador.numero_documento,
                        objTrabajador.telefono,
                        objTrabajador.rol,
                        objTrabajador.fecha_inicio,
                        objTrabajador.fecha_fin,
                        objTrabajador.sede_id,
                        objTrabajador.registrado_por,
                    ))
                connection.commit()
            return True
        return False
    except pymysql.err.IntegrityError as e:
        if e.args[0] == 1452:
            return 'Tu sede asignada ya no existe en el sistema (puede haber cambiado). Cierra sesión, vuelve a iniciar sesión y vuelve a intentarlo.'
        return e.args[1]
    except pymysql.MySQLError as e:
        return e.args[1]


def listar_trabajadores():
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "SELECT t.`id`, t.`nombre`, t.`apellido`, "
                        "t.`tipo_documento`, t.`numero_documento`, "
                        "t.`rol`, t.`fecha_inicio`, t.`fecha_fin`, "
                        + ESTADO_ROL_CASE + " AS `estado_rol`, "
                        "s.`nombre` AS `sede`, "
                        "u.`username` AS `registrado_por` "
                        "FROM `trabajadores` t "
                        "LEFT JOIN `sedes` s ON t.`sede_id` = s.`id` "
                        "LEFT JOIN `usuarios` u ON t.`registrado_por` = u.`id`"
                    )
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    return result
        return None
    except:
        return None


def listar_trabajadores_filtrado(sede_id_fijo=None, fecha_desde=None, fecha_hasta=None,
                                 sede_id=None, rol=None, estado=None,
                                 pagina=1, por_pagina=20):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    base = (
                        "SELECT t.`id`, t.`nombre`, t.`apellido`, "
                        "t.`tipo_documento`, t.`numero_documento`, "
                        "t.`rol`, t.`fecha_inicio`, t.`fecha_fin`, "
                        + ESTADO_ROL_CASE + " AS `estado_rol`, "
                        "s.`nombre` AS `sede`, "
                        "u.`username` AS `registrado_por`, t.`created_at` "
                        "FROM `trabajadores` t "
                        "LEFT JOIN `sedes` s ON t.`sede_id` = s.`id` "
                        "LEFT JOIN `usuarios` u ON t.`registrado_por` = u.`id` "
                        "WHERE 1=1 "
                    )
                    params = []

                    if sede_id_fijo:
                        base += "AND t.`sede_id` = %s "
                        params.append(sede_id_fijo)
                    if fecha_desde:
                        base += "AND t.`fecha_inicio` >= %s "
                        params.append(fecha_desde)
                    if fecha_hasta:
                        base += "AND t.`fecha_inicio` <= %s "
                        params.append(fecha_hasta)
                    if sede_id:
                        base += "AND t.`sede_id` = %s "
                        params.append(sede_id)
                    if rol:
                        base += "AND t.`rol` LIKE %s "
                        params.append("%" + rol + "%")
                    cond_estado = _condicion_estado(estado)
                    if cond_estado:
                        base += "AND (" + cond_estado + ") "

                    count_sql = "SELECT COUNT(*) AS total FROM (" + base + ") sub"
                    cursor.execute(count_sql, params)
                    total = cursor.fetchone()['total']

                    offset = (pagina - 1) * por_pagina
                    base += "ORDER BY t.`created_at` DESC LIMIT %s OFFSET %s"
                    params.append(por_pagina)
                    params.append(offset)

                    cursor.execute(base, params)
                    registros = cursor.fetchall()
                    return registros, total
        return [], 0
    except:
        return [], 0


def contar_trabajadores_resumen(sede_id_fijo=None):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "SELECT " + ESTADO_ROL_CASE + " AS `estado_rol`, COUNT(*) AS `cantidad` "
                        "FROM `trabajadores` t "
                        "WHERE 1=1 "
                    )
                    params = []
                    if sede_id_fijo:
                        sql += "AND t.`sede_id` = %s "
                        params.append(sede_id_fijo)
                    sql += "GROUP BY `estado_rol`"

                    cursor.execute(sql, params)
                    filas = cursor.fetchall()

                    conteo = {'vigente': 0, 'vencido': 0, 'sin_fecha_fin': 0}
                    for fila in filas:
                        conteo[fila['estado_rol']] = fila['cantidad']
                    conteo['total'] = sum(conteo.values())
                    return conteo
        return {'vigente': 0, 'vencido': 0, 'sin_fecha_fin': 0, 'total': 0}
    except:
        return {'vigente': 0, 'vencido': 0, 'sin_fecha_fin': 0, 'total': 0}


def listar_trabajadores_x_sede(sede_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "SELECT t.`id`, t.`nombre`, t.`apellido`, "
                        "t.`tipo_documento`, t.`numero_documento`, "
                        "t.`rol`, t.`fecha_inicio`, t.`fecha_fin`, "
                        + ESTADO_ROL_CASE + " AS `estado_rol`, "
                        "s.`nombre` AS `sede`, "
                        "u.`username` AS `registrado_por` "
                        "FROM `trabajadores` t "
                        "LEFT JOIN `sedes` s ON t.`sede_id` = s.`id` "
                        "LEFT JOIN `usuarios` u ON t.`registrado_por` = u.`id` "
                        "WHERE t.`sede_id` = %s"
                    )
                    cursor.execute(sql, sede_id)
                    return cursor.fetchall()
        return None
    except:
        return None


def obtener_trabajador_x_id(p_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "SELECT `id`, `nombre`, `apellido`, "
                        "`tipo_documento`, `numero_documento`, "
                        "`telefono`, `rol`, `fecha_inicio`, `fecha_fin`, "
                        "`sede_id`, `registrado_por` "
                        "FROM `trabajadores` WHERE `id` = %s"
                    )
                    cursor.execute(sql, p_id)
                    result = cursor.fetchall()
                    return result
        return None
    except:
        raise


def actualizar_trabajador(objTrabajador: Trabajador):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "UPDATE `trabajadores` "
                        "SET `nombre` = %s, `apellido` = %s, "
                        "`tipo_documento` = %s, `numero_documento` = %s, "
                        "`telefono` = %s, `rol` = %s, "
                        "`fecha_inicio` = %s, `fecha_fin` = %s, "
                        "`sede_id` = %s, `registrado_por` = %s "
                        "WHERE `id` = %s"
                    )
                    cursor.execute(sql, (
                        objTrabajador.nombre,
                        objTrabajador.apellido,
                        objTrabajador.tipo_documento,
                        objTrabajador.numero_documento,
                        objTrabajador.telefono,
                        objTrabajador.rol,
                        objTrabajador.fecha_inicio,
                        objTrabajador.fecha_fin,
                        objTrabajador.sede_id,
                        objTrabajador.registrado_por,
                        objTrabajador.id,
                    ))
                connection.commit()
            return True
        return False
    except pymysql.err.IntegrityError as e:
        if e.args[0] == 1452:
            return 'Tu sede asignada ya no existe en el sistema (puede haber cambiado). Cierra sesión, vuelve a iniciar sesión y vuelve a intentarlo.'
        return e.args[1]
    except pymysql.MySQLError as e:
        return e.args[1]


def eliminar_trabajador(p_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = "DELETE FROM `trabajadores` WHERE `id` = %s"
                    cursor.execute(sql, p_id)
                connection.commit()
            return True
        return False
    except pymysql.MySQLError as e:
        return e.args[1]
