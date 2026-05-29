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
                        "SELECT `id`, `nombre_completo`, `username`, `rol`, `sede_id`, `activo` "
                        "FROM `usuarios`"
                    )
                    cursor.execute(sql)
                    return cursor.fetchall()
        return None
    except:
        return None


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
