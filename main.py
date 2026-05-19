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