import pymysql

from usuarioClass import Usuario
from conexionBD import obtenerconexion


def insertar_usuario(objUsuario: Usuario):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "INSERT INTO `usuarios` "
                        "(`nombre_completo`, `username`, `password`, `rol`, `sede_id`, `activo`) "
                        "VALUES (%s, %s, %s, %s, %s, %s)"
                    )
                    cursor.execute(sql, (
                        objUsuario.nombre_completo,
                        objUsuario.username,
                        objUsuario.password,
                        objUsuario.rol,
                        objUsuario.sede_id,
                        objUsuario.activo,
                    ))
                connection.commit()
            return True
        return False
    except pymysql.MySQLError as e:
        return e.args[1]


def listar_usuarios():
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "SELECT u.`id`, u.`nombre_completo`, u.`username`, u.`rol`, "
                        "s.`nombre` AS `sede`, u.`activo` "
                        "FROM `usuarios` u "
                        "LEFT JOIN `sedes` s ON u.`sede_id` = s.`id`"
                    )
                    cursor.execute(sql)
                    return cursor.fetchall()
        return None
    except:
        return None


def contar_usuarios_activos():
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT COUNT(*) AS `total` FROM `usuarios` WHERE `activo` = 1")
                    return cursor.fetchone()['total']
        return 0
    except:
        return 0


def listar_usuarios_filtrado(sede_id=None, rol=None, activo=None, pagina=1, por_pagina=20):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    base = (
                        "SELECT u.`id`, u.`nombre_completo`, u.`username`, u.`rol`, "
                        "s.`nombre` AS `sede`, u.`activo` "
                        "FROM `usuarios` u "
                        "LEFT JOIN `sedes` s ON u.`sede_id` = s.`id` "
                        "WHERE 1=1 "
                    )
                    params = []

                    if sede_id:
                        base += "AND u.`sede_id` = %s "
                        params.append(sede_id)
                    if rol:
                        base += "AND u.`rol` = %s "
                        params.append(rol)
                    if activo is not None and activo != '':
                        base += "AND u.`activo` = %s "
                        params.append(activo)

                    count_sql = "SELECT COUNT(*) AS total FROM (" + base + ") sub"
                    cursor.execute(count_sql, params)
                    total = cursor.fetchone()['total']

                    offset = (pagina - 1) * por_pagina
                    base += "ORDER BY u.`nombre_completo` ASC LIMIT %s OFFSET %s"
                    params.append(por_pagina)
                    params.append(offset)

                    cursor.execute(base, params)
                    registros = cursor.fetchall()
                    return registros, total
        return [], 0
    except:
        return [], 0


def obtener_usuario_x_id(p_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "SELECT `id`, `nombre_completo`, `username`, `password`, `rol`, `sede_id`, `activo` "
                        "FROM `usuarios` WHERE `id` = %s"
                    )
                    cursor.execute(sql, p_id)
                    return cursor.fetchall()
        return None
    except:
        raise


def actualizar_usuario(objUsuario: Usuario):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "UPDATE `usuarios` "
                        "SET `nombre_completo` = %s, `username` = %s, `password` = %s, "
                        "`rol` = %s, `sede_id` = %s, `activo` = %s "
                        "WHERE `id` = %s"
                    )
                    cursor.execute(sql, (
                        objUsuario.nombre_completo,
                        objUsuario.username,
                        objUsuario.password,
                        objUsuario.rol,
                        objUsuario.sede_id,
                        objUsuario.activo,
                        objUsuario.id,
                    ))
                connection.commit()
            return True
        return False
    except pymysql.MySQLError as e:
        return e.args[1]


def eliminar_usuario(p_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = "DELETE FROM `usuarios` WHERE `id` = %s"
                    cursor.execute(sql, p_id)
                connection.commit()
            return True
        return False
    except pymysql.err.IntegrityError as e:
        if e.args[0] == 1451:
            return 'No se puede eliminar el usuario porque tiene registros asociados.'
        return e.args[1]
    except pymysql.MySQLError as e:
        return e.args[1]
