import json
from datetime import datetime

import pymysql

from ticketClass import Ticket
from conexionBD import obtenerconexion


# -----------------------------------------------
# Historial de comentarios embebido como JSON en `comentario_admin`.
# Cada entrada: {"autor", "rol", "fecha", "texto"}.
# Se mantiene retrocompatibilidad con comentarios antiguos en texto plano.
def parsear_historial_comentarios(valor_crudo):
    if not valor_crudo:
        return []
    try:
        datos = json.loads(valor_crudo)
        if isinstance(datos, list):
            return datos
        # Un JSON que no es lista: lo tratamos como texto plano
    except (ValueError, TypeError):
        pass
    # Comentario antiguo en texto plano: lo envolvemos como una entrada legacy
    texto = str(valor_crudo).strip()
    if not texto:
        return []
    return [{
        'autor': 'Sistema',
        'rol': '',
        'fecha': '',
        'texto': texto,
    }]


def _serializar_historial(historial):
    return json.dumps(historial, ensure_ascii=False)

# -----------------------------------------------
def insertar_ticket(objTicket: Ticket):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "INSERT INTO `tickets` "
                        "(`titulo`, `descripcion`, `categoria`, `prioridad`, "
                        "`equipo_afectado`, `cantidad_equipos`, "
                        "`nombre_contacto`, `telefono_contacto`, "
                        "`sede_id`, `creado_por`) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    )
                    cursor.execute(sql, (
                        objTicket.titulo,
                        objTicket.descripcion,
                        objTicket.categoria,
                        objTicket.prioridad,
                        objTicket.equipo_afectado,
                        objTicket.cantidad_equipos,
                        objTicket.nombre_contacto,
                        objTicket.telefono_contacto,
                        objTicket.sede_id,
                        objTicket.creado_por,
                    ))
                connection.commit()
            return True
        return False
    except pymysql.MySQLError as e:
        return e.args[1]


def listar_tickets():
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "SELECT t.`id`, t.`titulo`, t.`categoria`, t.`prioridad`, "
                        "t.`estado`, t.`equipo_afectado`, t.`nombre_contacto`, "
                        "s.`nombre` AS `sede`, u.`username` AS `creado_por` "
                        "FROM `tickets` t "
                        "LEFT JOIN `sedes` s ON t.`sede_id` = s.`id` "
                        "LEFT JOIN `usuarios` u ON t.`creado_por` = u.`id`"
                    )
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    return result
        return None
    except:
        return None


def listar_tickets_filtrado(sede_id_fijo=None, fecha_desde=None, fecha_hasta=None,
                            sede_id=None, prioridad=None, estado=None, categoria=None,
                            pagina=1, por_pagina=20):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    base = (
                        "SELECT t.`id`, t.`titulo`, t.`categoria`, t.`prioridad`, "
                        "t.`estado`, t.`equipo_afectado`, t.`nombre_contacto`, "
                        "s.`nombre` AS `sede`, u.`username` AS `creado_por`, "
                        "t.`created_at` "
                        "FROM `tickets` t "
                        "LEFT JOIN `sedes` s ON t.`sede_id` = s.`id` "
                        "LEFT JOIN `usuarios` u ON t.`creado_por` = u.`id` "
                        "WHERE 1=1 "
                    )
                    params = []

                    if sede_id_fijo:
                        base += "AND t.`sede_id` = %s "
                        params.append(sede_id_fijo)
                    if fecha_desde:
                        base += "AND DATE(t.`created_at`) >= %s "
                        params.append(fecha_desde)
                    if fecha_hasta:
                        base += "AND DATE(t.`created_at`) <= %s "
                        params.append(fecha_hasta)
                    if sede_id:
                        base += "AND t.`sede_id` = %s "
                        params.append(sede_id)
                    if prioridad:
                        base += "AND t.`prioridad` = %s "
                        params.append(prioridad)
                    if estado:
                        base += "AND t.`estado` = %s "
                        params.append(estado)
                    if categoria:
                        base += "AND t.`categoria` = %s "
                        params.append(categoria)

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


def contar_tickets_por_estado(sede_id_fijo=None):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "SELECT t.`estado`, COUNT(*) AS `cantidad` "
                        "FROM `tickets` t "
                        "WHERE 1=1 "
                    )
                    params = []
                    if sede_id_fijo:
                        sql += "AND t.`sede_id` = %s "
                        params.append(sede_id_fijo)
                    sql += "GROUP BY t.`estado`"

                    cursor.execute(sql, params)
                    filas = cursor.fetchall()

                    conteo = {'pendiente': 0, 'en_proceso': 0, 'resuelto': 0}
                    for fila in filas:
                        conteo[fila['estado']] = fila['cantidad']
                    conteo['total'] = sum(conteo.values())
                    return conteo
        return {'pendiente': 0, 'en_proceso': 0, 'resuelto': 0, 'total': 0}
    except:
        return {'pendiente': 0, 'en_proceso': 0, 'resuelto': 0, 'total': 0}


def listar_tickets_x_sede(sede_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "SELECT t.`id`, t.`titulo`, t.`categoria`, t.`prioridad`, "
                        "t.`estado`, t.`equipo_afectado`, t.`nombre_contacto`, "
                        "s.`nombre` AS `sede`, u.`username` AS `creado_por` "
                        "FROM `tickets` t "
                        "LEFT JOIN `sedes` s ON t.`sede_id` = s.`id` "
                        "LEFT JOIN `usuarios` u ON t.`creado_por` = u.`id` "
                        "WHERE t.`sede_id` = %s"
                    )
                    cursor.execute(sql, sede_id)
                    return cursor.fetchall()
        return None
    except:
        return None


def obtener_ticket_detalle(p_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "SELECT t.`id`, t.`titulo`, t.`descripcion`, t.`categoria`, "
                        "t.`prioridad`, t.`estado`, t.`comentario_admin`, "
                        "t.`equipo_afectado`, t.`cantidad_equipos`, "
                        "t.`nombre_contacto`, t.`telefono_contacto`, "
                        "t.`fecha_limite`, t.`created_at`, t.`updated_at`, "
                        "t.`resuelto_at`, t.`confirmado_at`, "
                        "s.`nombre` AS `sede`, "
                        "uc.`nombre_completo` AS `creado_por`, "
                        "ur.`nombre_completo` AS `resuelto_por`, "
                        "us.`nombre_completo` AS `confirmado_por` "
                        "FROM `tickets` t "
                        "LEFT JOIN `sedes` s ON t.`sede_id` = s.`id` "
                        "LEFT JOIN `usuarios` uc ON t.`creado_por` = uc.`id` "
                        "LEFT JOIN `usuarios` ur ON t.`resuelto_por` = ur.`id` "
                        "LEFT JOIN `usuarios` us ON t.`confirmado_por` = us.`id` "
                        "WHERE t.`id` = %s"
                    )
                    cursor.execute(sql, p_id)
                    return cursor.fetchone()
        return None
    except:
        raise


def cambiar_estado_ticket(p_id, estado, resuelto_por_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    if estado == 'resuelto':
                        sql = (
                            "UPDATE `tickets` "
                            "SET `estado` = %s, "
                            "`resuelto_por` = %s, `resuelto_at` = NOW() "
                            "WHERE `id` = %s"
                        )
                        cursor.execute(sql, (estado, resuelto_por_id, p_id))
                    else:
                        # Si el ticket sale de 'resuelto', se invalida la
                        # confirmacion previa del supervisor (ya no esta finalizado).
                        sql = (
                            "UPDATE `tickets` "
                            "SET `estado` = %s, "
                            "`confirmado_por` = NULL, `confirmado_at` = NULL "
                            "WHERE `id` = %s"
                        )
                        cursor.execute(sql, (estado, p_id))
                connection.commit()
            return True
        return False
    except pymysql.MySQLError as e:
        return e.args[1]


def confirmar_ticket(p_id, supervisor_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT `estado` FROM `tickets` WHERE `id` = %s", p_id)
                    fila = cursor.fetchone()
                    if fila is None:
                        return 'Ticket no encontrado.'
                    # Solo se puede confirmar un ticket ya finalizado (resuelto).
                    if fila['estado'] != 'resuelto':
                        return 'Solo se puede confirmar un ticket resuelto.'

                    cursor.execute(
                        "UPDATE `tickets` "
                        "SET `confirmado_por` = %s, `confirmado_at` = NOW() "
                        "WHERE `id` = %s",
                        (supervisor_id, p_id)
                    )
                connection.commit()
            return True
        return False
    except pymysql.MySQLError as e:
        return e.args[1]


def agregar_comentario_ticket(p_id, texto, autor, rol):
    texto = (texto or '').strip()
    if not texto:
        return 'El comentario no puede estar vacio.'
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT `comentario_admin` FROM `tickets` WHERE `id` = %s",
                        p_id
                    )
                    fila = cursor.fetchone()
                    if fila is None:
                        return 'Ticket no encontrado.'

                    historial = parsear_historial_comentarios(fila['comentario_admin'])
                    historial.append({
                        'autor': autor or 'Usuario',
                        'rol': rol or '',
                        'fecha': datetime.now().strftime('%Y-%m-%d %H:%M'),
                        'texto': texto,
                    })

                    cursor.execute(
                        "UPDATE `tickets` SET `comentario_admin` = %s WHERE `id` = %s",
                        (_serializar_historial(historial), p_id)
                    )
                connection.commit()
            return True
        return False
    except pymysql.MySQLError as e:
        return e.args[1]


def obtener_ticket_x_id(p_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "SELECT `id`, `titulo`, `descripcion`, `categoria`, `prioridad`, "
                        "`equipo_afectado`, `cantidad_equipos`, "
                        "`nombre_contacto`, `telefono_contacto`, "
                        "`sede_id`, `creado_por` "
                        "FROM `tickets` WHERE `id` = %s"
                    )
                    cursor.execute(sql, p_id)
                    result = cursor.fetchall()
                    return result
        return None
    except:
        raise


def actualizar_ticket(objTicket: Ticket):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = (
                        "UPDATE `tickets` "
                        "SET `titulo` = %s, `descripcion` = %s, `categoria` = %s, "
                        "`prioridad` = %s, `equipo_afectado` = %s, `cantidad_equipos` = %s, "
                        "`nombre_contacto` = %s, `telefono_contacto` = %s, "
                        "`sede_id` = %s, `creado_por` = %s "
                        "WHERE `id` = %s"
                    )
                    cursor.execute(sql, (
                        objTicket.titulo,
                        objTicket.descripcion,
                        objTicket.categoria,
                        objTicket.prioridad,
                        objTicket.equipo_afectado,
                        objTicket.cantidad_equipos,
                        objTicket.nombre_contacto,
                        objTicket.telefono_contacto,
                        objTicket.sede_id,
                        objTicket.creado_por,
                        objTicket.id,
                    ))
                connection.commit()
            return True
        return False
    except pymysql.MySQLError as e:
        return e.args[1]


def eliminar_ticket(p_id):
    try:
        connection = obtenerconexion()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    sql = "DELETE FROM `tickets` WHERE `id` = %s"
                    cursor.execute(sql, p_id)
                connection.commit()
            return True
        return False
    except pymysql.MySQLError as e:
        return e.args[1]


