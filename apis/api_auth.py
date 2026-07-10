from types import SimpleNamespace

from conexionBD import obtenerconexion


def authenticate(username, password):
    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = (
                "SELECT `id`, `nombre_completo`, `username`, `rol`, `sede_id`, `activo` "
                "FROM `usuarios` "
                "WHERE `username` = %s AND `password` = %s AND `activo` = 1"
            )
            cursor.execute(sql, (username, password))
            usuario = cursor.fetchone()

    if usuario is None:
        return None
    return SimpleNamespace(**usuario)


def identity(payload):
    user_id = payload['identity']

    connection = obtenerconexion()
    with connection:
        with connection.cursor() as cursor:
            sql = (
                "SELECT `id`, `nombre_completo`, `username`, `rol`, `sede_id`, `activo` "
                "FROM `usuarios` WHERE `id` = %s"
            )
            cursor.execute(sql, (user_id,))
            usuario = cursor.fetchone()

    if usuario is None:
        return None
    return SimpleNamespace(**usuario)
