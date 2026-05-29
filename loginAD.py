import pymysql

from loginClass import Login
from conexionBD import obtenerconexion


def listar_usuarios():
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = "SELECT `id`, `username` FROM `usuarios` WHERE `activo` = 1"
                    cursor.execute(sql)
                    return cursor.fetchall()
        return []
    except:
        return []


def verificar_login(objLogin: Login):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM `usuarios` WHERE `username` = %s AND `password` = %s AND `activo` = 1"
                    cursor.execute(sql, (objLogin.username, objLogin.password))
                    resultado = cursor.fetchone()
            return resultado
        return False
    except pymysql.MySQLError as e:
        return e.args[1]
