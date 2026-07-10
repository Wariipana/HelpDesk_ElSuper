import pymysql

from solicitudClienteClass import SolicitudCliente
from conexionBD import obtenerconexion


def insertar_solicitud_cliente(objSolicitud: SolicitudCliente):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "INSERT INTO `solicitudes_cliente` "
                        "(`nombre_cliente`, `apellido_cliente`, "
                        "`tipo_documento`, `numero_documento`, "
                        "`telefono_cliente`, `email_cliente`, "
                        "`tipo`, `motivo`, `sede_id`, `solicitado_por`) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    )
                    cursor.execute(sql, (
                        objSolicitud.nombre_cliente,
                        objSolicitud.apellido_cliente,
                        objSolicitud.tipo_documento,
                        objSolicitud.numero_documento,
                        objSolicitud.telefono_cliente,
                        objSolicitud.email_cliente,
                        objSolicitud.tipo,
                        objSolicitud.motivo,
                        objSolicitud.sede_id,
                        objSolicitud.solicitado_por,
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


def listar_solicitudes_cliente():
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "SELECT sc.`id`, sc.`nombre_cliente`, sc.`apellido_cliente`, "
                        "sc.`tipo_documento`, sc.`numero_documento`, "
                        "sc.`tipo`, sc.`estado`, s.`nombre` AS `sede`, "
                        "u.`username` AS `solicitado_por` "
                        "FROM `solicitudes_cliente` sc "
                        "LEFT JOIN `sedes` s ON sc.`sede_id` = s.`id` "
                        "LEFT JOIN `usuarios` u ON sc.`solicitado_por` = u.`id`"
                    )
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    return result
        return None
    except:
        return None


def listar_solicitudes_filtrado(sede_id_fijo=None, fecha_desde=None, fecha_hasta=None,
                                sede_id=None, tipo=None, estado=None,
                                pagina=1, por_pagina=20):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    base = (
                        "SELECT sc.`id`, sc.`nombre_cliente`, sc.`apellido_cliente`, "
                        "sc.`tipo_documento`, sc.`numero_documento`, "
                        "sc.`tipo`, sc.`estado`, s.`nombre` AS `sede`, "
                        "u.`username` AS `solicitado_por`, sc.`created_at` "
                        "FROM `solicitudes_cliente` sc "
                        "LEFT JOIN `sedes` s ON sc.`sede_id` = s.`id` "
                        "LEFT JOIN `usuarios` u ON sc.`solicitado_por` = u.`id` "
                        "WHERE 1=1 "
                    )
                    params = []

                    if sede_id_fijo:
                        base += "AND sc.`sede_id` = %s "
                        params.append(sede_id_fijo)
                    if fecha_desde:
                        base += "AND DATE(sc.`created_at`) >= %s "
                        params.append(fecha_desde)
                    if fecha_hasta:
                        base += "AND DATE(sc.`created_at`) <= %s "
                        params.append(fecha_hasta)
                    if sede_id:
                        base += "AND sc.`sede_id` = %s "
                        params.append(sede_id)
                    if tipo:
                        base += "AND sc.`tipo` = %s "
                        params.append(tipo)
                    if estado:
                        base += "AND sc.`estado` = %s "
                        params.append(estado)

                    count_sql = "SELECT COUNT(*) AS total FROM (" + base + ") sub"
                    cursor.execute(count_sql, params)
                    total = cursor.fetchone()['total']

                    offset = (pagina - 1) * por_pagina
                    base += "ORDER BY sc.`created_at` DESC LIMIT %s OFFSET %s"
                    params.append(por_pagina)
                    params.append(offset)

                    cursor.execute(base, params)
                    registros = cursor.fetchall()
                    return registros, total
        return [], 0
    except:
        return [], 0


def contar_solicitudes_por_estado(sede_id_fijo=None):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "SELECT sc.`estado`, COUNT(*) AS `cantidad` "
                        "FROM `solicitudes_cliente` sc "
                        "WHERE 1=1 "
                    )
                    params = []
                    if sede_id_fijo:
                        sql += "AND sc.`sede_id` = %s "
                        params.append(sede_id_fijo)
                    sql += "GROUP BY sc.`estado`"

                    cursor.execute(sql, params)
                    filas = cursor.fetchall()

                    conteo = {'pendiente': 0, 'aprobado': 0, 'rechazado': 0}
                    for fila in filas:
                        conteo[fila['estado']] = fila['cantidad']
                    conteo['total'] = sum(conteo.values())
                    return conteo
        return {'pendiente': 0, 'aprobado': 0, 'rechazado': 0, 'total': 0}
    except:
        return {'pendiente': 0, 'aprobado': 0, 'rechazado': 0, 'total': 0}


def listar_solicitudes_x_sede(sede_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "SELECT sc.`id`, sc.`nombre_cliente`, sc.`apellido_cliente`, "
                        "sc.`tipo_documento`, sc.`numero_documento`, "
                        "sc.`tipo`, sc.`estado`, s.`nombre` AS `sede`, "
                        "u.`username` AS `solicitado_por` "
                        "FROM `solicitudes_cliente` sc "
                        "LEFT JOIN `sedes` s ON sc.`sede_id` = s.`id` "
                        "LEFT JOIN `usuarios` u ON sc.`solicitado_por` = u.`id` "
                        "WHERE sc.`sede_id` = %s"
                    )
                    cursor.execute(sql, sede_id)
                    return cursor.fetchall()
        return None
    except:
        return None


def obtener_solicitud_detalle(p_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "SELECT sc.`id`, sc.`nombre_cliente`, sc.`apellido_cliente`, "
                        "sc.`tipo_documento`, sc.`numero_documento`, "
                        "sc.`telefono_cliente`, sc.`email_cliente`, "
                        "sc.`tipo`, sc.`motivo`, sc.`estado`, sc.`observacion_admin`, "
                        "sc.`created_at`, sc.`updated_at`, sc.`resuelto_at`, "
                        "s.`nombre` AS `sede`, "
                        "us.`nombre_completo` AS `solicitado_por`, "
                        "ur.`nombre_completo` AS `resuelto_por` "
                        "FROM `solicitudes_cliente` sc "
                        "LEFT JOIN `sedes` s ON sc.`sede_id` = s.`id` "
                        "LEFT JOIN `usuarios` us ON sc.`solicitado_por` = us.`id` "
                        "LEFT JOIN `usuarios` ur ON sc.`resuelto_por` = ur.`id` "
                        "WHERE sc.`id` = %s"
                    )
                    cursor.execute(sql, p_id)
                    return cursor.fetchone()
        return None
    except:
        raise


def gestionar_solicitud(p_id, estado, observacion, resuelto_por_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    if estado in ('aprobado', 'rechazado'):
                        sql = (
                            "UPDATE `solicitudes_cliente` "
                            "SET `estado` = %s, `observacion_admin` = %s, "
                            "`resuelto_por` = %s, `resuelto_at` = NOW() "
                            "WHERE `id` = %s"
                        )
                        cursor.execute(sql, (estado, observacion, resuelto_por_id, p_id))
                    else:
                        sql = (
                            "UPDATE `solicitudes_cliente` "
                            "SET `estado` = %s, `observacion_admin` = %s "
                            "WHERE `id` = %s"
                        )
                        cursor.execute(sql, (estado, observacion, p_id))
                connection.commit()
            return True
        return False
    except pymysql.MySQLError as e:
        return e.args[1]


def obtener_solicitud_cliente_x_id(p_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "SELECT `id`, `nombre_cliente`, `apellido_cliente`, "
                        "`tipo_documento`, `numero_documento`, "
                        "`telefono_cliente`, `email_cliente`, "
                        "`tipo`, `motivo`, `estado`, `observacion_admin`, "
                        "`sede_id`, `solicitado_por` "
                        "FROM `solicitudes_cliente` WHERE `id` = %s"
                    )
                    cursor.execute(sql, p_id)
                    result = cursor.fetchall()
                    return result
        return None
    except:
        raise


def actualizar_solicitud_cliente(objSolicitud: SolicitudCliente):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "UPDATE `solicitudes_cliente` "
                        "SET `nombre_cliente` = %s, `apellido_cliente` = %s, "
                        "`tipo_documento` = %s, `numero_documento` = %s, "
                        "`telefono_cliente` = %s, `email_cliente` = %s, "
                        "`tipo` = %s, `motivo` = %s, `sede_id` = %s, `solicitado_por` = %s "
                        "WHERE `id` = %s"
                    )
                    cursor.execute(sql, (
                        objSolicitud.nombre_cliente,
                        objSolicitud.apellido_cliente,
                        objSolicitud.tipo_documento,
                        objSolicitud.numero_documento,
                        objSolicitud.telefono_cliente,
                        objSolicitud.email_cliente,
                        objSolicitud.tipo,
                        objSolicitud.motivo,
                        objSolicitud.sede_id,
                        objSolicitud.solicitado_por,
                        objSolicitud.id,
                    ))
                connection.commit()
            return True
        return False
    except pymysql.MySQLError as e:
        return e.args[1]


def eliminar_solicitud_cliente(p_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = "DELETE FROM `solicitudes_cliente` WHERE `id` = %s"
                    cursor.execute(sql, p_id)
                connection.commit()
            return True
        return False
    except pymysql.MySQLError as e:
        return e.args[1]
