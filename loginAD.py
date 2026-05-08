import pymysql

from loginClass import Login


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
