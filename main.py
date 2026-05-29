import pymysql
from flask import render_template, Flask, request, redirect

from loginClass import Login
from loginAD import verificar_login, listar_usuarios as listar_usuarios_login

from usuarioClass import Usuario
from usuarioAD import insertar_usuario, listar_usuarios, obtener_usuario_x_id, actualizar_usuario, eliminar_usuario
from loginAD import verificar_login, listar_usuarios as listar_usuarios_login

from usuarioClass import Usuario
from usuarioAD import insertar_usuario, listar_usuarios, obtener_usuario_x_id, actualizar_usuario, eliminar_usuario

from sedeClass import Sede
from sedeAD import insertar_sede, listar_sedes, obtener_sede_x_id, actualizar_sede, eliminar_sede

from ticketClass import Ticket
from ticketAD import insertar_ticket, listar_tickets, obtener_ticket_x_id, actualizar_ticket, eliminar_ticket

from solicitudClienteClass import SolicitudCliente
from solicitudClienteAD import insertar_solicitud_cliente, listar_solicitudes_cliente, obtener_solicitud_cliente_x_id, actualizar_solicitud_cliente, eliminar_solicitud_cliente

from movimientoEquipoClass import MovimientoEquipo
from movimientoEquipoAD import insertar_movimiento_equipo, listar_movimientos_equipo, obtener_movimiento_equipo_x_id, actualizar_movimiento_equipo, eliminar_movimiento_equipo

app = Flask(__name__)

# Cuando lo ocasiona el usuario
@app.errorhandler(400)
def error_400(e):
    return render_template('error400.html'), 400

# Cuando lo ocasiona el servidor
@app.errorhandler(500)
def error_500(e):
    return render_template('error500.html'), 500


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
                return redirect('/dashboard')
            elif res == False:
                return render_template('form_login.html', error='Problemas con la conexion. Intenta de nuevo.')
                return render_template('form_login.html', error='Problemas con la conexion. Intenta de nuevo.')
            else:
                return render_template('form_login.html', error='Usuario o contrasena incorrectos.')
                return render_template('form_login.html', error='Usuario o contrasena incorrectos.')

        except:
            return render_template('form_login.html', error='Ocurrio un error inesperado. Intenta de nuevo.')
            return render_template('form_login.html', error='Ocurrio un error inesperado. Intenta de nuevo.')

    else:

        return redirect('/login')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


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
        return render_template('error400.html', mensaje=res, url_volver='/listar-sedes'), 400
    except:
        return render_template('error500.html'), 500
        return render_template('error500.html'), 500


@app.route('/ticket')
def form_ticket():
    sedes = listar_sedes()
    usuarios = listar_usuarios_login()
    return render_template('form_ticket.html', sedes=sedes, usuarios=usuarios)
    sedes = listar_sedes()
    usuarios = listar_usuarios_login()
    return render_template('form_ticket.html', sedes=sedes, usuarios=usuarios)


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
                request.form.get('sede_id'),
                request.form.get('creado_por')
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
    resultado = listar_tickets()
    return render_template('lista_tickets.html', tickets=resultado)


@app.route('/cargar-formulario-editar-ticket/<int:id_ticket>')
def cargar_formulario_editar_ticket(id_ticket):
    resultado = obtener_ticket_x_id(id_ticket)
    sedes = listar_sedes()
    usuarios = listar_usuarios_login()
    return render_template('form_ticket_edit.html', ticket=resultado[0], sedes=sedes, usuarios=usuarios)
    sedes = listar_sedes()
    usuarios = listar_usuarios_login()
    return render_template('form_ticket_edit.html', ticket=resultado[0], sedes=sedes, usuarios=usuarios)


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
                request.form.get('sede_id'),
                request.form.get('creado_por'),
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
        return render_template('error400.html', mensaje=res, url_volver='/listar-tickets'), 400
    except:
        return render_template('error500.html'), 500
        return render_template('error500.html'), 500


@app.route('/solicitud-cliente')
def form_solicitud_cliente():
    sedes = listar_sedes()
    usuarios = listar_usuarios_login()
    return render_template('form_solicitud_cliente.html', sedes=sedes, usuarios=usuarios)
    sedes = listar_sedes()
    usuarios = listar_usuarios_login()
    return render_template('form_solicitud_cliente.html', sedes=sedes, usuarios=usuarios)


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
                request.form.get('sede_id'),
                request.form.get('solicitado_por')
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
    resultado = listar_solicitudes_cliente()
    return render_template('lista_solicitudes_cliente.html', solicitudes=resultado)


@app.route('/cargar-formulario-editar-solicitud-cliente/<int:id_solicitud>')
def cargar_formulario_editar_solicitud_cliente(id_solicitud):
    resultado = obtener_solicitud_cliente_x_id(id_solicitud)
    sedes = listar_sedes()
    usuarios = listar_usuarios_login()
    return render_template('form_solicitud_cliente_edit.html', solicitud=resultado[0], sedes=sedes, usuarios=usuarios)
    sedes = listar_sedes()
    usuarios = listar_usuarios_login()
    return render_template('form_solicitud_cliente_edit.html', solicitud=resultado[0], sedes=sedes, usuarios=usuarios)


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
                request.form.get('sede_id'),
                request.form.get('solicitado_por'),
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
        return render_template('error400.html', mensaje=res, url_volver='/listar-solicitudes-cliente'), 400
    except:
        return render_template('error500.html'), 500
        return render_template('error500.html'), 500


@app.route('/movimiento-equipo')
def form_movimiento_equipo():
    sedes = listar_sedes()
    usuarios = listar_usuarios_login()
    return render_template('form_movimiento_equipo.html', sedes=sedes, usuarios=usuarios)
    sedes = listar_sedes()
    usuarios = listar_usuarios_login()
    return render_template('form_movimiento_equipo.html', sedes=sedes, usuarios=usuarios)


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
                request.form.get('registrado_por')
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
    resultado = listar_movimientos_equipo()
    return render_template('lista_movimientos_equipo.html', movimientos=resultado)


@app.route('/cargar-formulario-editar-movimiento-equipo/<int:id_movimiento>')
def cargar_formulario_editar_movimiento_equipo(id_movimiento):
    resultado = obtener_movimiento_equipo_x_id(id_movimiento)
    sedes = listar_sedes()
    usuarios = listar_usuarios_login()
    return render_template('form_movimiento_equipo_edit.html', movimiento=resultado[0], sedes=sedes, usuarios=usuarios)
    sedes = listar_sedes()
    usuarios = listar_usuarios_login()
    return render_template('form_movimiento_equipo_edit.html', movimiento=resultado[0], sedes=sedes, usuarios=usuarios)


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
                request.form.get('registrado_por'),
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
    resultado = listar_usuarios()
    return render_template('lista_usuarios.html', usuarios=resultado)


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
