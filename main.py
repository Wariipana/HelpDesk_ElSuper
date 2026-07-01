import pymysql
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
from flask import render_template, Flask, request, redirect, session, url_for

from chatbot_helpdesk import encontrar_respuesta as chatbot_respuesta
from apis import registrar_apis
from reportes import generar_reporte

# Registros suficientes para exportar todos los datos de un modulo sin paginar
POR_PAGINA_REPORTE = 100000

from loginClass import Login
from loginAD import verificar_login, listar_usuarios as listar_usuarios_login

from usuarioClass import Usuario
from usuarioAD import insertar_usuario, listar_usuarios, listar_usuarios_filtrado, obtener_usuario_x_id, actualizar_usuario, eliminar_usuario

from sedeClass import Sede
from sedeAD import insertar_sede, listar_sedes, obtener_sede_x_id, actualizar_sede, eliminar_sede

from ticketClass import Ticket
from ticketAD import insertar_ticket, listar_tickets, listar_tickets_x_sede, listar_tickets_filtrado, obtener_ticket_x_id, actualizar_ticket, eliminar_ticket, obtener_ticket_detalle, gestionar_ticket, contar_tickets_por_estado

from solicitudClienteClass import SolicitudCliente
from solicitudClienteAD import (insertar_solicitud_cliente, listar_solicitudes_cliente,
    listar_solicitudes_x_sede, listar_solicitudes_filtrado, obtener_solicitud_cliente_x_id, obtener_solicitud_detalle,
    actualizar_solicitud_cliente, eliminar_solicitud_cliente, gestionar_solicitud)

from movimientoEquipoClass import MovimientoEquipo
from movimientoEquipoAD import insertar_movimiento_equipo, listar_movimientos_equipo, listar_movimientos_filtrado, obtener_movimiento_equipo_x_id, actualizar_movimiento_equipo, eliminar_movimiento_equipo

from trabajadorClass import Trabajador
from trabajadorAD import (insertar_trabajador, listar_trabajadores,
    listar_trabajadores_x_sede, listar_trabajadores_filtrado, obtener_trabajador_x_id,
    actualizar_trabajador, eliminar_trabajador)

app = Flask(__name__)
app.secret_key = 'elsuper_helpdesk_secret_2024'
app.config['JWT_SECRET_KEY'] = 'elsuper_helpdesk_jwt_2024'
registrar_apis(app)

# Cuando lo ocasiona el usuario
@app.errorhandler(400)
def error_400(e):
    return render_template('error400.html'), 400

# Cuando lo ocasiona el servidor
@app.errorhandler(500)
def error_500(e):
    return render_template('error500.html'), 500

@app.route('/chatbot', methods=['POST'])
def chatbot():
    pregunta = request.form.get('pregunta', '').strip()
    if pregunta:
        conversacion = session.setdefault('chatbot_conversacion', [])
        conversacion.append({'tipo': 'usuario', 'texto': pregunta})
        conversacion.append({'tipo': 'bot', 'texto': chatbot_respuesta(pregunta)})
        session.modified = True

    referrer = request.referrer or url_for('dashboard')
    parsed = urlparse(referrer)
    params = parse_qs(parsed.query)
    params.pop('chatbot', None)
    params['chatbot'] = ['open']
    return redirect(urlunparse(parsed._replace(query=urlencode(params, doseq=True))))


@app.route('/chatbot/limpiar', methods=['POST'])
def chatbot_limpiar():
    session.pop('chatbot_conversacion', None)
    session.modified = True
    return redirect(request.referrer or url_for('dashboard'))


@app.route('/')
def index():
    return redirect('/login')


@app.route('/login')
def form_login():
    return render_template('form_login.html')


@app.route('/login', methods=['POST'])
def hacer_login():

    if request.method == 'POST':

        try:

            objLogin = Login(
                request.form.get('username'),
                request.form.get('password')
            )

            res = verificar_login(objLogin)

            if res:
                session['usuario_id']      = res['id']
                session['usuario_nombre']  = res['nombre_completo']
                session['usuario_rol']     = res['rol']
                session['usuario_sede_id'] = res['sede_id']
                session['usuario_sede']    = res['sede']
                return redirect('/dashboard')
            elif res == False:
                return render_template('form_login.html', error='Problemas con la conexion. Intenta de nuevo.')
            else:
                return render_template('form_login.html', error='Usuario o contrasena incorrectos.')
        except:
            return render_template('form_login.html', error='Ocurrio un error inesperado. Intenta de nuevo.')
    else:

        return redirect('/login')


@app.route('/dashboard')
def dashboard():
    rol = session.get('usuario_rol')
    sede_id_fijo = session.get('usuario_sede_id') if rol == 'admin_tienda' else None
    conteo_tickets = contar_tickets_por_estado(sede_id_fijo=sede_id_fijo or None)
    return render_template('dashboard.html', conteo_tickets=conteo_tickets)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/sede')
def form_sede():
    return render_template('form_sede.html')


@app.route('/guardar-sede', methods=['POST'])
def guardar_sede():

    if request.method == 'POST':

        try:

            objSede = Sede(
                request.form.get('nombre'),
                request.form.get('direccion')
            )

            res = insertar_sede(objSede)

            if res == True:
                return render_template('exito_sede.html')
            elif res == False:
                return render_template('error400.html', mensaje='Problemas en la insercion.'), 400
            else:
                return render_template('error400.html', mensaje=res), 400

        except:
            return render_template('error500.html'), 500

    else:

        return redirect('/sede')


@app.route('/listar-sedes')
def listar_sedes_view():
    resultado = listar_sedes()
    return render_template('lista_sedes.html', sedes=resultado)


@app.route('/cargar-formulario-editar-sede/<int:id_sede>')
def cargar_formulario_editar_sede(id_sede):
    resultado = obtener_sede_x_id(id_sede)
    return render_template('form_sede_edit.html', sede=resultado[0])


@app.route('/actualizar-sede', methods=['POST'])
def actualizar_sede_view():

    if request.method == 'POST':

        try:

            objSede = Sede(
                request.form.get('nombre'),
                request.form.get('direccion'),
                request.form.get('id')
            )

            res = actualizar_sede(objSede)

            if res == True:
                return render_template('exito_sede.html')
            elif res == False:
                return render_template('error400.html', mensaje='Problemas en la actualizacion.'), 400
            else:
                return render_template('error400.html', mensaje=res), 400

        except:
            return render_template('error500.html'), 500

    else:

        return redirect('/listar-sedes')


@app.route('/eliminar-sede/<int:id_sede>')
def eliminar_sede_view(id_sede):
    try:
        res = eliminar_sede(id_sede)
        if res == True:
            return redirect('/listar-sedes')
        return render_template('error400.html', mensaje=res, url_volver='/listar-sedes'), 400
    except:
        return render_template('error500.html'), 500


@app.route('/ticket')
def form_ticket():
    return render_template('form_ticket.html')


@app.route('/guardar-ticket', methods=['POST'])
def guardar_ticket():

    if request.method == 'POST':

        try:

            objTicket = Ticket(
                request.form.get('titulo'),
                request.form.get('descripcion'),
                request.form.get('categoria'),
                request.form.get('prioridad'),
                request.form.get('equipo_afectado'),
                request.form.get('cantidad_equipos'),
                request.form.get('nombre_contacto'),
                request.form.get('telefono_contacto'),
                session.get('usuario_sede_id'),
                session.get('usuario_id')
            )

            res = insertar_ticket(objTicket)

            if res == True:
                return render_template('exito_ticket.html')
            elif res == False:
                return render_template('error400.html', mensaje='Problemas en la insercion.'), 400
            else:
                return render_template('error400.html', mensaje=res), 400

        except:
            return render_template('error500.html'), 500

    else:

        return redirect('/ticket')


@app.route('/listar-tickets')
def listar_tickets_view():
    rol = session.get('usuario_rol')
    sede_id_fijo = session.get('usuario_sede_id') if rol == 'admin_tienda' else None

    fecha_desde  = request.args.get('fecha_desde', '').strip()
    fecha_hasta  = request.args.get('fecha_hasta', '').strip()
    sede_id      = request.args.get('sede_id', '').strip()
    prioridad    = request.args.get('prioridad', '').strip()
    estado       = request.args.get('estado', '').strip()
    categoria    = request.args.get('categoria', '').strip()
    pagina       = int(request.args.get('pagina', 1))

    tickets, total = listar_tickets_filtrado(
        sede_id_fijo = sede_id_fijo or None,
        fecha_desde  = fecha_desde  or None,
        fecha_hasta  = fecha_hasta  or None,
        sede_id      = sede_id      or None,
        prioridad    = prioridad    or None,
        estado       = estado       or None,
        categoria    = categoria    or None,
        pagina       = pagina,
        por_pagina   = 20
    )

    por_pagina    = 20
    total_paginas = max(1, -(-total // por_pagina))
    sedes         = listar_sedes() if rol != 'admin_tienda' else []

    filtros = {
        'fecha_desde': fecha_desde, 'fecha_hasta': fecha_hasta,
        'sede_id': sede_id, 'prioridad': prioridad,
        'estado': estado, 'categoria': categoria,
    }

    return render_template('lista_tickets.html',
        tickets=tickets, sedes=sedes, filtros=filtros,
        pagina=pagina, total_paginas=total_paginas, total=total)


@app.route('/reporte-tickets')
def reporte_tickets():
    rol = session.get('usuario_rol')
    sede_id_fijo = session.get('usuario_sede_id') if rol == 'admin_tienda' else None

    tickets, _ = listar_tickets_filtrado(
        sede_id_fijo = sede_id_fijo or None,
        fecha_desde  = request.args.get('fecha_desde', '').strip() or None,
        fecha_hasta  = request.args.get('fecha_hasta', '').strip() or None,
        sede_id      = request.args.get('sede_id', '').strip() or None,
        prioridad    = request.args.get('prioridad', '').strip() or None,
        estado       = request.args.get('estado', '').strip() or None,
        categoria    = request.args.get('categoria', '').strip() or None,
        pagina       = 1,
        por_pagina   = POR_PAGINA_REPORTE
    )

    columnas = [
        {'clave': 'id',              'titulo': 'ID',              'peso': 0.5},
        {'clave': 'titulo',          'titulo': 'Titulo',          'peso': 2.5},
        {'clave': 'categoria',       'titulo': 'Categoria',       'peso': 1},
        {'clave': 'prioridad',       'titulo': 'Prioridad',       'peso': 1},
        {'clave': 'estado',          'titulo': 'Estado',          'peso': 1},
        {'clave': 'equipo_afectado', 'titulo': 'Equipo afectado', 'peso': 2},
        {'clave': 'nombre_contacto', 'titulo': 'Contacto',        'peso': 1.5},
        {'clave': 'sede',            'titulo': 'Sede',            'peso': 1.5},
        {'clave': 'creado_por',      'titulo': 'Creado por',      'peso': 1.2},
        {'clave': 'created_at',      'titulo': 'Fecha',           'peso': 1.3},
    ]

    formato = request.args.get('formato', 'csv').strip().lower()
    return generar_reporte(formato, 'tickets', 'Reporte de Tickets', columnas, tickets)


@app.route('/cargar-formulario-editar-ticket/<int:id_ticket>')
def cargar_formulario_editar_ticket(id_ticket):
    resultado = obtener_ticket_x_id(id_ticket)
    return render_template('form_ticket_edit.html', ticket=resultado[0])


@app.route('/actualizar-ticket', methods=['POST'])
def actualizar_ticket_view():

    if request.method == 'POST':

        try:

            objTicket = Ticket(
                request.form.get('titulo'),
                request.form.get('descripcion'),
                request.form.get('categoria'),
                request.form.get('prioridad'),
                request.form.get('equipo_afectado'),
                request.form.get('cantidad_equipos'),
                request.form.get('nombre_contacto'),
                request.form.get('telefono_contacto'),
                session.get('usuario_sede_id'),
                session.get('usuario_id'),
                request.form.get('id')
            )

            res = actualizar_ticket(objTicket)

            if res == True:
                return render_template('exito_ticket.html')
            elif res == False:
                return render_template('error400.html', mensaje='Problemas en la actualizacion.'), 400
            else:
                return render_template('error400.html', mensaje=res), 400

        except:
            return render_template('error500.html'), 500

    else:

        return redirect('/listar-tickets')


@app.route('/eliminar-ticket/<int:id_ticket>')
def eliminar_ticket_view(id_ticket):
    try:
        res = eliminar_ticket(id_ticket)
        if res == True:
            return redirect('/listar-tickets')
        return render_template('error400.html', mensaje=res, url_volver='/listar-tickets'), 400
    except:
        return render_template('error500.html'), 500


@app.route('/gestionar-ticket/<int:id_ticket>')
def gestionar_ticket_view(id_ticket):
    ticket = obtener_ticket_detalle(id_ticket)
    if not ticket:
        return render_template('error400.html', mensaje='Ticket no encontrado.', url_volver='/listar-tickets'), 400
    return render_template('detalle_ticket.html', ticket=ticket)


@app.route('/gestionar-ticket/<int:id_ticket>', methods=['POST'])
def guardar_gestion_ticket(id_ticket):
    try:
        estado     = request.form.get('estado')
        comentario = request.form.get('comentario_admin', '').strip()
        res = gestionar_ticket(id_ticket, estado, comentario, session.get('usuario_id'))
        if res == True:
            return redirect('/listar-tickets')
        return render_template('error400.html', mensaje=res, url_volver='/listar-tickets'), 400
    except:
        return render_template('error500.html'), 500


@app.route('/solicitud-cliente')
def form_solicitud_cliente():
    return render_template('form_solicitud_cliente.html')


@app.route('/guardar-solicitud-cliente', methods=['POST'])
def guardar_solicitud_cliente():

    if request.method == 'POST':

        try:

            objSolicitud = SolicitudCliente(
                request.form.get('nombre_cliente'),
                request.form.get('apellido_cliente'),
                request.form.get('tipo_documento'),
                request.form.get('numero_documento'),
                request.form.get('telefono_cliente'),
                request.form.get('email_cliente'),
                request.form.get('tipo'),
                request.form.get('motivo'),
                session.get('usuario_sede_id'),
                session.get('usuario_id')
            )

            res = insertar_solicitud_cliente(objSolicitud)

            if res == True:
                return render_template('exito_solicitud_cliente.html')
            elif res == False:
                return render_template('error400.html', mensaje='Problemas en la insercion.'), 400
            else:
                return render_template('error400.html', mensaje=res), 400

        except:
            return render_template('error500.html'), 500

    else:

        return redirect('/solicitud-cliente')


@app.route('/listar-solicitudes-cliente')
def listar_solicitudes_cliente_view():
    rol = session.get('usuario_rol')
    sede_id_fijo = session.get('usuario_sede_id') if rol == 'admin_tienda' else None

    fecha_desde = request.args.get('fecha_desde', '').strip()
    fecha_hasta = request.args.get('fecha_hasta', '').strip()
    sede_id     = request.args.get('sede_id', '').strip()
    tipo        = request.args.get('tipo', '').strip()
    estado      = request.args.get('estado', '').strip()
    pagina      = int(request.args.get('pagina', 1))

    solicitudes, total = listar_solicitudes_filtrado(
        sede_id_fijo = sede_id_fijo or None,
        fecha_desde  = fecha_desde  or None,
        fecha_hasta  = fecha_hasta  or None,
        sede_id      = sede_id      or None,
        tipo         = tipo         or None,
        estado       = estado       or None,
        pagina       = pagina,
        por_pagina   = 20
    )

    por_pagina    = 20
    total_paginas = max(1, -(-total // por_pagina))
    sedes         = listar_sedes() if rol != 'admin_tienda' else []

    filtros = {
        'fecha_desde': fecha_desde, 'fecha_hasta': fecha_hasta,
        'sede_id': sede_id, 'tipo': tipo, 'estado': estado,
    }

    return render_template('lista_solicitudes_cliente.html',
        solicitudes=solicitudes, sedes=sedes, filtros=filtros,
        pagina=pagina, total_paginas=total_paginas, total=total)


@app.route('/reporte-solicitudes-cliente')
def reporte_solicitudes_cliente():
    rol = session.get('usuario_rol')
    sede_id_fijo = session.get('usuario_sede_id') if rol == 'admin_tienda' else None

    solicitudes, _ = listar_solicitudes_filtrado(
        sede_id_fijo = sede_id_fijo or None,
        fecha_desde  = request.args.get('fecha_desde', '').strip() or None,
        fecha_hasta  = request.args.get('fecha_hasta', '').strip() or None,
        sede_id      = request.args.get('sede_id', '').strip() or None,
        tipo         = request.args.get('tipo', '').strip() or None,
        estado       = request.args.get('estado', '').strip() or None,
        pagina       = 1,
        por_pagina   = POR_PAGINA_REPORTE
    )

    columnas = [
        {'clave': 'id',               'titulo': 'ID',             'peso': 0.5},
        {'clave': 'nombre_cliente',   'titulo': 'Nombre',         'peso': 1.5},
        {'clave': 'apellido_cliente', 'titulo': 'Apellido',       'peso': 1.5},
        {'clave': 'tipo_documento',   'titulo': 'Tipo doc.',      'peso': 1},
        {'clave': 'numero_documento', 'titulo': 'Nro. documento', 'peso': 1.3},
        {'clave': 'tipo',             'titulo': 'Tipo',           'peso': 1.2},
        {'clave': 'estado',           'titulo': 'Estado',         'peso': 1},
        {'clave': 'sede',             'titulo': 'Sede',           'peso': 1.5},
        {'clave': 'solicitado_por',   'titulo': 'Solicitado por', 'peso': 1.3},
        {'clave': 'created_at',       'titulo': 'Fecha',          'peso': 1.3},
    ]

    formato = request.args.get('formato', 'csv').strip().lower()
    return generar_reporte(formato, 'solicitudes_cliente',
                           'Reporte de Solicitudes de Cliente', columnas, solicitudes)


@app.route('/cargar-formulario-editar-solicitud-cliente/<int:id_solicitud>')
def cargar_formulario_editar_solicitud_cliente(id_solicitud):
    resultado = obtener_solicitud_cliente_x_id(id_solicitud)
    return render_template('form_solicitud_cliente_edit.html', solicitud=resultado[0])


@app.route('/actualizar-solicitud-cliente', methods=['POST'])
def actualizar_solicitud_cliente_view():

    if request.method == 'POST':

        try:

            objSolicitud = SolicitudCliente(
                request.form.get('nombre_cliente'),
                request.form.get('apellido_cliente'),
                request.form.get('tipo_documento'),
                request.form.get('numero_documento'),
                request.form.get('telefono_cliente'),
                request.form.get('email_cliente'),
                request.form.get('tipo'),
                request.form.get('motivo'),
                session.get('usuario_sede_id'),
                session.get('usuario_id'),
                request.form.get('id')
            )

            res = actualizar_solicitud_cliente(objSolicitud)

            if res == True:
                return render_template('exito_solicitud_cliente.html')
            elif res == False:
                return render_template('error400.html', mensaje='Problemas en la actualizacion.'), 400
            else:
                return render_template('error400.html', mensaje=res), 400

        except:
            return render_template('error500.html'), 500

    else:

        return redirect('/listar-solicitudes-cliente')


@app.route('/eliminar-solicitud-cliente/<int:id_solicitud>')
def eliminar_solicitud_cliente_view(id_solicitud):
    try:
        res = eliminar_solicitud_cliente(id_solicitud)
        if res == True:
            return redirect('/listar-solicitudes-cliente')
        return render_template('error400.html', mensaje=res, url_volver='/listar-solicitudes-cliente'), 400
    except:
        return render_template('error500.html'), 500


@app.route('/gestionar-solicitud/<int:id_solicitud>')
def gestionar_solicitud_view(id_solicitud):
    solicitud = obtener_solicitud_detalle(id_solicitud)
    if not solicitud:
        return render_template('error400.html', mensaje='Solicitud no encontrada.', url_volver='/listar-solicitudes-cliente'), 400
    return render_template('detalle_solicitud_cliente.html', solicitud=solicitud)


@app.route('/gestionar-solicitud/<int:id_solicitud>', methods=['POST'])
def guardar_gestion_solicitud(id_solicitud):
    try:
        estado      = request.form.get('estado')
        observacion = request.form.get('observacion_admin', '').strip()
        res = gestionar_solicitud(id_solicitud, estado, observacion, session.get('usuario_id'))
        if res == True:
            return redirect('/listar-solicitudes-cliente')
        return render_template('error400.html', mensaje=res, url_volver='/listar-solicitudes-cliente'), 400
    except:
        return render_template('error500.html'), 500


@app.route('/trabajador')
def form_trabajador():
    return render_template('form_trabajador.html')


@app.route('/guardar-trabajador', methods=['POST'])
def guardar_trabajador():

    if request.method == 'POST':

        try:

            objTrabajador = Trabajador(
                request.form.get('nombre'),
                request.form.get('apellido'),
                request.form.get('tipo_documento'),
                request.form.get('numero_documento'),
                request.form.get('telefono'),
                request.form.get('rol'),
                request.form.get('fecha_inicio'),
                request.form.get('fecha_fin') or None,
                session.get('usuario_sede_id'),
                session.get('usuario_id')
            )

            res = insertar_trabajador(objTrabajador)

            if res == True:
                return render_template('exito_trabajador.html')
            elif res == False:
                return render_template('error400.html', mensaje='Problemas en la insercion.'), 400
            else:
                return render_template('error400.html', mensaje=res), 400

        except:
            return render_template('error500.html'), 500

    else:

        return redirect('/trabajador')


@app.route('/listar-trabajadores')
def listar_trabajadores_view():
    rol_usuario = session.get('usuario_rol')
    sede_id_fijo = session.get('usuario_sede_id') if rol_usuario == 'admin_tienda' else None

    fecha_desde = request.args.get('fecha_desde', '').strip()
    fecha_hasta = request.args.get('fecha_hasta', '').strip()
    sede_id     = request.args.get('sede_id', '').strip()
    rol         = request.args.get('rol', '').strip()
    estado      = request.args.get('estado', '').strip()
    pagina      = int(request.args.get('pagina', 1))

    trabajadores, total = listar_trabajadores_filtrado(
        sede_id_fijo = sede_id_fijo or None,
        fecha_desde  = fecha_desde  or None,
        fecha_hasta  = fecha_hasta  or None,
        sede_id      = sede_id      or None,
        rol          = rol          or None,
        estado       = estado       or None,
        pagina       = pagina,
        por_pagina   = 20
    )

    por_pagina    = 20
    total_paginas = max(1, -(-total // por_pagina))
    sedes         = listar_sedes() if rol_usuario != 'admin_tienda' else []

    filtros = {
        'fecha_desde': fecha_desde, 'fecha_hasta': fecha_hasta,
        'sede_id': sede_id, 'rol': rol, 'estado': estado,
    }

    return render_template('lista_trabajadores.html',
        trabajadores=trabajadores, sedes=sedes, filtros=filtros,
        pagina=pagina, total_paginas=total_paginas, total=total)


@app.route('/reporte-trabajadores')
def reporte_trabajadores():
    rol_usuario = session.get('usuario_rol')
    sede_id_fijo = session.get('usuario_sede_id') if rol_usuario == 'admin_tienda' else None

    trabajadores, _ = listar_trabajadores_filtrado(
        sede_id_fijo = sede_id_fijo or None,
        fecha_desde  = request.args.get('fecha_desde', '').strip() or None,
        fecha_hasta  = request.args.get('fecha_hasta', '').strip() or None,
        sede_id      = request.args.get('sede_id', '').strip() or None,
        rol          = request.args.get('rol', '').strip() or None,
        estado       = request.args.get('estado', '').strip() or None,
        pagina       = 1,
        por_pagina   = POR_PAGINA_REPORTE
    )

    columnas = [
        {'clave': 'id',              'titulo': 'ID',             'peso': 0.5},
        {'clave': 'nombre',          'titulo': 'Nombre',         'peso': 1.5},
        {'clave': 'apellido',        'titulo': 'Apellido',       'peso': 1.5},
        {'clave': 'tipo_documento',  'titulo': 'Tipo doc.',      'peso': 1},
        {'clave': 'numero_documento','titulo': 'Nro. documento', 'peso': 1.3},
        {'clave': 'rol',             'titulo': 'Rol',            'peso': 2},
        {'clave': 'fecha_inicio',    'titulo': 'Fecha inicio',   'peso': 1.2},
        {'clave': 'fecha_fin',       'titulo': 'Fecha fin',      'peso': 1.2},
        {'clave': 'estado_rol',      'titulo': 'Estado',         'peso': 1},
        {'clave': 'sede',            'titulo': 'Sede',           'peso': 1.5},
        {'clave': 'registrado_por',  'titulo': 'Registrado por', 'peso': 1.3},
    ]

    formato = request.args.get('formato', 'csv').strip().lower()
    return generar_reporte(formato, 'trabajadores',
                           'Reporte de Trabajadores', columnas, trabajadores)


@app.route('/cargar-formulario-editar-trabajador/<int:id_trabajador>')
def cargar_formulario_editar_trabajador(id_trabajador):
    resultado = obtener_trabajador_x_id(id_trabajador)
    return render_template('form_trabajador_edit.html', trabajador=resultado[0])


@app.route('/actualizar-trabajador', methods=['POST'])
def actualizar_trabajador_view():

    if request.method == 'POST':

        try:

            objTrabajador = Trabajador(
                request.form.get('nombre'),
                request.form.get('apellido'),
                request.form.get('tipo_documento'),
                request.form.get('numero_documento'),
                request.form.get('telefono'),
                request.form.get('rol'),
                request.form.get('fecha_inicio'),
                request.form.get('fecha_fin') or None,
                session.get('usuario_sede_id'),
                session.get('usuario_id'),
                request.form.get('id')
            )

            res = actualizar_trabajador(objTrabajador)

            if res == True:
                return render_template('exito_trabajador.html')
            elif res == False:
                return render_template('error400.html', mensaje='Problemas en la actualizacion.'), 400
            else:
                return render_template('error400.html', mensaje=res), 400

        except:
            return render_template('error500.html'), 500

    else:

        return redirect('/listar-trabajadores')


@app.route('/eliminar-trabajador/<int:id_trabajador>')
def eliminar_trabajador_view(id_trabajador):
    try:
        res = eliminar_trabajador(id_trabajador)
        if res == True:
            return redirect('/listar-trabajadores')
        return render_template('error400.html', mensaje=res, url_volver='/listar-trabajadores'), 400
    except:
        return render_template('error500.html'), 500


@app.route('/movimiento-equipo')
def form_movimiento_equipo():
    sedes = listar_sedes()
    return render_template('form_movimiento_equipo.html', sedes=sedes)


@app.route('/guardar-movimiento-equipo', methods=['POST'])
def guardar_movimiento_equipo():

    if request.method == 'POST':

        try:

            objMovimiento = MovimientoEquipo(
                request.form.get('tipo'),
                request.form.get('tipo_equipo'),
                request.form.get('modelo'),
                request.form.get('numero_serie'),
                request.form.get('sede_id'),
                request.form.get('responsable'),
                request.form.get('fecha'),
                session.get('usuario_id')
            )

            res = insertar_movimiento_equipo(objMovimiento)

            if res == True:
                return render_template('exito_movimiento_equipo.html')
            elif res == False:
                return render_template('error400.html', mensaje='Problemas en la insercion.'), 400
            else:
                return render_template('error400.html', mensaje=res), 400

        except:
            return render_template('error500.html'), 500

    else:

        return redirect('/movimiento-equipo')


@app.route('/listar-movimientos-equipo')
def listar_movimientos_equipo_view():
    fecha_desde = request.args.get('fecha_desde', '').strip()
    fecha_hasta = request.args.get('fecha_hasta', '').strip()
    sede_id     = request.args.get('sede_id', '').strip()
    tipo        = request.args.get('tipo', '').strip()
    tipo_equipo = request.args.get('tipo_equipo', '').strip()
    pagina      = int(request.args.get('pagina', 1))

    movimientos, total = listar_movimientos_filtrado(
        fecha_desde = fecha_desde or None,
        fecha_hasta = fecha_hasta or None,
        sede_id     = sede_id     or None,
        tipo        = tipo        or None,
        tipo_equipo = tipo_equipo or None,
        pagina      = pagina,
        por_pagina  = 20
    )

    por_pagina    = 20
    total_paginas = max(1, -(-total // por_pagina))
    sedes         = listar_sedes()

    filtros = {
        'fecha_desde': fecha_desde, 'fecha_hasta': fecha_hasta,
        'sede_id': sede_id, 'tipo': tipo, 'tipo_equipo': tipo_equipo,
    }

    return render_template('lista_movimientos_equipo.html',
        movimientos=movimientos, sedes=sedes, filtros=filtros,
        pagina=pagina, total_paginas=total_paginas, total=total)


@app.route('/reporte-movimientos-equipo')
def reporte_movimientos_equipo():
    movimientos, _ = listar_movimientos_filtrado(
        fecha_desde = request.args.get('fecha_desde', '').strip() or None,
        fecha_hasta = request.args.get('fecha_hasta', '').strip() or None,
        sede_id     = request.args.get('sede_id', '').strip() or None,
        tipo        = request.args.get('tipo', '').strip() or None,
        tipo_equipo = request.args.get('tipo_equipo', '').strip() or None,
        pagina      = 1,
        por_pagina  = POR_PAGINA_REPORTE
    )

    columnas = [
        {'clave': 'id',             'titulo': 'ID',             'peso': 0.5},
        {'clave': 'tipo',           'titulo': 'Tipo',           'peso': 1.2},
        {'clave': 'tipo_equipo',    'titulo': 'Tipo equipo',    'peso': 1.3},
        {'clave': 'modelo',         'titulo': 'Modelo',         'peso': 1.8},
        {'clave': 'numero_serie',   'titulo': 'Nro. serie',     'peso': 1.5},
        {'clave': 'sede',           'titulo': 'Sede',           'peso': 1.5},
        {'clave': 'responsable',    'titulo': 'Responsable',    'peso': 1.8},
        {'clave': 'fecha',          'titulo': 'Fecha',          'peso': 1.2},
        {'clave': 'registrado_por', 'titulo': 'Registrado por', 'peso': 1.3},
    ]

    formato = request.args.get('formato', 'csv').strip().lower()
    return generar_reporte(formato, 'movimientos_equipo',
                           'Reporte de Movimientos de Equipo', columnas, movimientos)


@app.route('/cargar-formulario-editar-movimiento-equipo/<int:id_movimiento>')
def cargar_formulario_editar_movimiento_equipo(id_movimiento):
    resultado = obtener_movimiento_equipo_x_id(id_movimiento)
    sedes = listar_sedes()
    return render_template('form_movimiento_equipo_edit.html', movimiento=resultado[0], sedes=sedes)


@app.route('/actualizar-movimiento-equipo', methods=['POST'])
def actualizar_movimiento_equipo_view():

    if request.method == 'POST':

        try:

            objMovimiento = MovimientoEquipo(
                request.form.get('tipo'),
                request.form.get('tipo_equipo'),
                request.form.get('modelo'),
                request.form.get('numero_serie'),
                request.form.get('sede_id'),
                request.form.get('responsable'),
                request.form.get('fecha'),
                session.get('usuario_id'),
                request.form.get('id')
            )

            res = actualizar_movimiento_equipo(objMovimiento)

            if res == True:
                return render_template('exito_movimiento_equipo.html')
            elif res == False:
                return render_template('error400.html', mensaje='Problemas en la actualizacion.'), 400
            else:
                return render_template('error400.html', mensaje=res), 400

        except:
            return render_template('error500.html'), 500

    else:

        return redirect('/listar-movimientos-equipo')


@app.route('/eliminar-movimiento-equipo/<int:id_movimiento>')
def eliminar_movimiento_equipo_view(id_movimiento):
    try:
        res = eliminar_movimiento_equipo(id_movimiento)
        if res == True:
            return redirect('/listar-movimientos-equipo')
        return render_template('error400.html', mensaje=res, url_volver='/listar-movimientos-equipo'), 400
    except:
        return render_template('error500.html'), 500


@app.route('/usuario')
def form_usuario():
    sedes = listar_sedes()
    return render_template('form_usuario.html', sedes=sedes)


@app.route('/guardar-usuario', methods=['POST'])
def guardar_usuario():

    if request.method == 'POST':

        try:

            objUsuario = Usuario(
                request.form.get('nombre_completo'),
                request.form.get('username'),
                request.form.get('password'),
                request.form.get('rol'),
                request.form.get('sede_id'),
                request.form.get('activo'),
            )

            res = insertar_usuario(objUsuario)

            if res == True:
                return render_template('exito_usuario.html')
            elif res == False:
                return render_template('error400.html', mensaje='Problemas en la insercion.'), 400
            else:
                return render_template('error400.html', mensaje=res), 400

        except:
            return render_template('error500.html'), 500

    else:

        return redirect('/usuario')


@app.route('/listar-usuarios')
def listar_usuarios_view():
    sede_id = request.args.get('sede_id', '').strip()
    rol     = request.args.get('rol', '').strip()
    activo  = request.args.get('activo', '').strip()
    pagina  = int(request.args.get('pagina', 1))

    usuarios, total = listar_usuarios_filtrado(
        sede_id    = sede_id or None,
        rol        = rol     or None,
        activo     = activo  if activo != '' else None,
        pagina     = pagina,
        por_pagina = 20
    )

    por_pagina    = 20
    total_paginas = max(1, -(-total // por_pagina))
    sedes         = listar_sedes()

    filtros = {'sede_id': sede_id, 'rol': rol, 'activo': activo}

    return render_template('lista_usuarios.html',
        usuarios=usuarios, sedes=sedes, filtros=filtros,
        pagina=pagina, total_paginas=total_paginas, total=total)


@app.route('/cargar-formulario-editar-usuario/<int:id_usuario>')
def cargar_formulario_editar_usuario(id_usuario):
    resultado = obtener_usuario_x_id(id_usuario)
    sedes = listar_sedes()
    return render_template('form_usuario_edit.html', usuario=resultado[0], sedes=sedes)


@app.route('/actualizar-usuario', methods=['POST'])
def actualizar_usuario_view():

    if request.method == 'POST':

        try:

            objUsuario = Usuario(
                request.form.get('nombre_completo'),
                request.form.get('username'),
                request.form.get('password'),
                request.form.get('rol'),
                request.form.get('sede_id'),
                request.form.get('activo'),
                request.form.get('id'),
            )

            res = actualizar_usuario(objUsuario)

            if res == True:
                return render_template('exito_usuario.html')
            elif res == False:
                return render_template('error400.html', mensaje='Problemas en la actualizacion.'), 400
            else:
                return render_template('error400.html', mensaje=res), 400

        except:
            return render_template('error500.html'), 500

    else:

        return redirect('/listar-usuarios')


@app.route('/eliminar-usuario/<int:id_usuario>')
def eliminar_usuario_view(id_usuario):
    try:
        res = eliminar_usuario(id_usuario)
        if res == True:
            return redirect('/listar-usuarios')
        return render_template('error400.html', mensaje=res, url_volver='/listar-usuarios'), 400
    except:
        return render_template('error500.html'), 500
