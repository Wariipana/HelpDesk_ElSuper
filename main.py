import pymysql
from flask import render_template, Flask, request, redirect

from loginClass import Login
from loginAD import verificar_login

from sedeClass import Sede
from sedeAD import insertar_sede, listar_sedes

from ticketClass import Ticket
from ticketAD import insertar_ticket, listar_tickets

from solicitudClienteClass import SolicitudCliente
from solicitudClienteAD import insertar_solicitud_cliente, listar_solicitudes_cliente

from movimientoEquipoClass import MovimientoEquipo
from movimientoEquipoAD import insertar_movimiento_equipo, listar_movimientos_equipo

app = Flask(__name__)


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
                return f'<p>Bienvenido, {res["nombre_completo"]} ({res["rol"]})</p>'
            elif res == False:
                return '<p>Problemas en la conexion</p>'
            else:
                return '<p>Usuario o contrasena incorrectos</p>'

        except:
            return '<p>Problemas en el procesamiento</p>'

    else:

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
                return '<p>Problemas en la insercion</p>'
            else:
                return f'<p>{res}</p>'

        except:
            return '<p>Problemas en el procesamiento</p>'

    else:

        return redirect('/sede')


@app.route('/listar-sedes')
def listar_sedes_view():
    resultado = listar_sedes()
    return render_template('lista_sedes.html', sedes=resultado)


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
                request.form.get('sede_id'),
                request.form.get('creado_por')
            )

            res = insertar_ticket(objTicket)

            if res == True:
                return render_template('exito_ticket.html')
            elif res == False:
                return '<p>Problemas en la insercion</p>'
            else:
                return f'<p>{res}</p>'

        except:
            return '<p>Problemas en el procesamiento</p>'

    else:

        return redirect('/ticket')


@app.route('/listar-tickets')
def listar_tickets_view():
    resultado = listar_tickets()
    return render_template('lista_tickets.html', tickets=resultado)


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
                request.form.get('sede_id'),
                request.form.get('solicitado_por')
            )

            res = insertar_solicitud_cliente(objSolicitud)

            if res == True:
                return render_template('exito_solicitud_cliente.html')
            elif res == False:
                return '<p>Problemas en la insercion</p>'
            else:
                return f'<p>{res}</p>'

        except:
            return '<p>Problemas en el procesamiento</p>'

    else:

        return redirect('/solicitud-cliente')


@app.route('/listar-solicitudes-cliente')
def listar_solicitudes_cliente_view():
    resultado = listar_solicitudes_cliente()
    return render_template('lista_solicitudes_cliente.html', solicitudes=resultado)


@app.route('/movimiento-equipo')
def form_movimiento_equipo():
    return render_template('form_movimiento_equipo.html')


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
                return '<p>Problemas en la insercion</p>'
            else:
                return f'<p>{res}</p>'

        except:
            return '<p>Problemas en el procesamiento</p>'

    else:

        return redirect('/movimiento-equipo')


@app.route('/listar-movimientos-equipo')
def listar_movimientos_equipo_view():
    resultado = listar_movimientos_equipo()
    return render_template('lista_movimientos_equipo.html', movimientos=resultado)
