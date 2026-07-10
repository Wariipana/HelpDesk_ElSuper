import re
from datetime import date, datetime


class ValidationError(Exception):
    def __init__(self, errores):
        if isinstance(errores, str):
            errores = [errores]
        self.errores = errores
        super().__init__('; '.join(errores))


_PATRON_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ][A-Za-zÁÉÍÓÚÜÑáéíóúüñ '\.\-]*$")
_PATRON_USERNAME = re.compile(r"^[A-Za-z0-9_.\-]+$")
_PATRON_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_PATRON_ENTERO = re.compile(r"^\d+$")
_PATRON_TELEFONO = re.compile(r"^\d{9}$")


# -----------------------------------------------
# Validadores atomicos: cada uno agrega su mensaje a `errores` y
# devuelve el valor ya limpio (o None si no es valido).
def _texto(valor, campo, errores, minimo=1, maximo=None, requerido=True):
    valor = (valor or '').strip()
    if not valor:
        if requerido:
            errores.append(campo + ': es obligatorio.')
        return None
    if len(valor) < minimo:
        errores.append(campo + ': debe tener al menos ' + str(minimo) + ' caracteres.')
        return None
    if maximo and len(valor) > maximo:
        errores.append(campo + ': no puede superar los ' + str(maximo) + ' caracteres.')
        return None
    return valor


def _nombre(valor, campo, errores, maximo=150):
    valor = _texto(valor, campo, errores, minimo=2, maximo=maximo)
    if valor is None:
        return None
    if not _PATRON_NOMBRE.match(valor):
        errores.append(campo + ': solo debe contener letras y espacios.')
        return None
    return valor


def _entero(valor, campo, errores, minimo=None, maximo=None, requerido=True):
    valor = (valor or '').strip()
    if not valor:
        if requerido:
            errores.append(campo + ': es obligatorio.')
        return None
    if not _PATRON_ENTERO.match(valor):
        errores.append(campo + ': debe ser un número entero válido.')
        return None
    numero = int(valor)
    if minimo is not None and numero < minimo:
        errores.append(campo + ': debe ser mayor o igual a ' + str(minimo) + '.')
        return None
    if maximo is not None and numero > maximo:
        errores.append(campo + ': debe ser menor o igual a ' + str(maximo) + '.')
        return None
    return numero


def _telefono(valor, campo, errores, requerido=True):
    valor = (valor or '').strip()
    if not valor:
        if requerido:
            errores.append(campo + ': es obligatorio.')
        return None
    if not _PATRON_TELEFONO.match(valor):
        errores.append(campo + ': debe tener exactamente 9 dígitos numéricos.')
        return None
    return valor


def _email(valor, campo, errores, requerido=True, maximo=150):
    valor = (valor or '').strip()
    if not valor:
        if requerido:
            errores.append(campo + ': es obligatorio.')
        return None
    if len(valor) > maximo or not _PATRON_EMAIL.match(valor):
        errores.append(campo + ': no tiene un formato de correo válido.')
        return None
    return valor


def _enum(valor, campo, opciones, errores, requerido=True):
    valor = (valor or '').strip()
    if not valor:
        if requerido:
            errores.append(campo + ': es obligatorio.')
        return None
    if valor not in opciones:
        errores.append(campo + ': valor no permitido.')
        return None
    return valor


def _fecha(valor, campo, errores, requerido=True):
    valor = (valor or '').strip()
    if not valor:
        if requerido:
            errores.append(campo + ': es obligatoria.')
        return None
    try:
        fecha = datetime.strptime(valor, '%Y-%m-%d').date()
    except ValueError:
        errores.append(campo + ': formato de fecha inválido (use AAAA-MM-DD).')
        return None
    if fecha.year < 1900 or fecha.year > 2100:
        errores.append(campo + ': el año debe estar entre 1900 y 2100.')
        return None
    return fecha


def _numero_documento(tipo_documento, valor, errores, campo='Número de documento'):
    valor = (valor or '').strip()
    if not valor:
        errores.append(campo + ': es obligatorio.')
        return None
    if tipo_documento == 'dni':
        if not re.fullmatch(r'\d{8}', valor):
            errores.append(campo + ': el DNI debe tener exactamente 8 dígitos numéricos.')
            return None
    elif tipo_documento == 'ruc':
        if not re.fullmatch(r'\d{11}', valor):
            errores.append(campo + ': el RUC debe tener exactamente 11 dígitos numéricos.')
            return None
    elif tipo_documento in ('ce', 'pasaporte', 'ptp', 'otro'):
        if not re.fullmatch(r'[A-Za-z0-9\-]{5,20}', valor):
            errores.append(campo + ': debe tener entre 5 y 20 caracteres alfanuméricos.')
            return None
    else:
        # tipo_documento invalido ya fue reportado por el validador de enum
        return None
    return valor


def validar_id(valor, campo='ID'):
    errores = []
    numero = _entero(valor, campo, errores, minimo=1)
    if errores:
        raise ValidationError(errores)
    return numero


def _sede_id(valor, campo, sedes_validas, errores, requerido=True):
    numero = _entero(valor, campo, errores, minimo=1, requerido=requerido)
    if numero is None:
        return None
    if sedes_validas is not None and numero not in sedes_validas:
        errores.append(campo + ': la sede seleccionada no existe.')
        return None
    return numero


# -----------------------------------------------
# Validadores por entidad. Cada uno recibe el `form` (request.form) y
# devuelve un dict con los valores ya limpios, o lanza ValidationError
# con la lista completa de problemas encontrados.
def validar_ticket(form, sede_fija=None, sedes_validas=None):
    errores = []
    datos = {}

    datos['titulo'] = _texto(form.get('titulo'), 'Título', errores, minimo=3, maximo=200)
    datos['descripcion'] = _texto(form.get('descripcion'), 'Descripción', errores, minimo=5, maximo=4000)
    datos['categoria'] = _enum(form.get('categoria'), 'Categoría',
        {'hardware', 'software', 'conectividad', 'otro'}, errores)
    datos['prioridad'] = _enum(form.get('prioridad'), 'Prioridad',
        {'baja', 'media', 'alta', 'critica'}, errores)
    datos['equipo_afectado'] = _texto(form.get('equipo_afectado'), 'Equipo afectado', errores, minimo=2, maximo=150)
    datos['cantidad_equipos'] = _entero(form.get('cantidad_equipos'), 'Cantidad de equipos', errores, minimo=1, maximo=255)
    datos['nombre_contacto'] = _nombre(form.get('nombre_contacto'), 'Nombre de contacto', errores)
    datos['telefono_contacto'] = _telefono(form.get('telefono_contacto'), 'Teléfono de contacto', errores)

    if sede_fija:
        datos['sede_id'] = sede_fija
    else:
        datos['sede_id'] = _sede_id(form.get('sede_id'), 'Sede', sedes_validas, errores)

    if errores:
        raise ValidationError(errores)
    return datos


def validar_solicitud_cliente(form, sede_fija=None, sedes_validas=None):
    errores = []
    datos = {}

    datos['nombre_cliente'] = _nombre(form.get('nombre_cliente'), 'Nombre del cliente', errores)
    datos['apellido_cliente'] = _nombre(form.get('apellido_cliente'), 'Apellido del cliente', errores)
    datos['tipo_documento'] = _enum(form.get('tipo_documento'), 'Tipo de documento',
        {'dni', 'ce', 'pasaporte', 'ruc', 'ptp', 'otro'}, errores)
    if datos['tipo_documento'] is not None:
        datos['numero_documento'] = _numero_documento(
            datos['tipo_documento'], form.get('numero_documento'), errores, 'Número de documento')
    else:
        datos['numero_documento'] = None
    datos['telefono_cliente'] = _telefono(form.get('telefono_cliente'), 'Teléfono del cliente', errores)
    datos['email_cliente'] = _email(form.get('email_cliente'), 'Email del cliente', errores)
    datos['tipo'] = _enum(form.get('tipo'), 'Tipo de solicitud', {'alta', 'baja'}, errores)
    datos['motivo'] = _texto(form.get('motivo'), 'Motivo', errores, minimo=5, maximo=2000)

    if sede_fija:
        datos['sede_id'] = sede_fija
    else:
        datos['sede_id'] = _sede_id(form.get('sede_id'), 'Sede', sedes_validas, errores)

    if errores:
        raise ValidationError(errores)
    return datos


def validar_movimiento_equipo(form, sedes_validas=None):
    errores = []
    datos = {}

    datos['tipo'] = _enum(form.get('tipo'), 'Tipo de movimiento', {'entrada', 'salida'}, errores)
    datos['tipo_equipo'] = _texto(form.get('tipo_equipo'), 'Tipo de equipo', errores, minimo=2, maximo=100)
    datos['modelo'] = _texto(form.get('modelo'), 'Modelo', errores, minimo=1, maximo=150)
    datos['numero_serie'] = _texto(form.get('numero_serie'), 'Número de serie', errores, minimo=1, maximo=100)
    datos['sede_id'] = _sede_id(form.get('sede_id'), 'Sede', sedes_validas, errores)
    datos['responsable'] = _nombre(form.get('responsable'), 'Responsable', errores)
    datos['fecha'] = _fecha(form.get('fecha'), 'Fecha del movimiento', errores)

    if errores:
        raise ValidationError(errores)
    return datos


def validar_trabajador(form, sede_fija=None, sedes_validas=None):
    errores = []
    datos = {}

    datos['nombre'] = _nombre(form.get('nombre'), 'Nombre', errores)
    datos['apellido'] = _nombre(form.get('apellido'), 'Apellido', errores)
    datos['tipo_documento'] = _enum(form.get('tipo_documento'), 'Tipo de documento',
        {'dni', 'ce', 'pasaporte', 'ruc', 'ptp', 'otro'}, errores)
    if datos['tipo_documento'] is not None:
        datos['numero_documento'] = _numero_documento(
            datos['tipo_documento'], form.get('numero_documento'), errores, 'Número de documento')
    else:
        datos['numero_documento'] = None
    datos['telefono'] = _telefono(form.get('telefono'), 'Teléfono', errores)
    datos['rol'] = _texto(form.get('rol'), 'Rol / Cargo', errores, minimo=2, maximo=100)

    datos['fecha_inicio'] = _fecha(form.get('fecha_inicio'), 'Fecha de inicio', errores)

    fecha_fin_raw = (form.get('fecha_fin') or '').strip()
    if fecha_fin_raw:
        datos['fecha_fin'] = _fecha(fecha_fin_raw, 'Fecha de fin', errores)
        if (datos['fecha_fin'] is not None and datos['fecha_inicio'] is not None
                and datos['fecha_fin'] < datos['fecha_inicio']):
            errores.append('Fecha de fin: no puede ser anterior a la fecha de inicio.')
    else:
        datos['fecha_fin'] = None

    if sede_fija:
        datos['sede_id'] = sede_fija
    else:
        datos['sede_id'] = _sede_id(form.get('sede_id'), 'Sede', sedes_validas, errores)

    if errores:
        raise ValidationError(errores)
    return datos


def validar_usuario(form, sedes_validas=None):
    errores = []
    datos = {}

    datos['nombre_completo'] = _nombre(form.get('nombre_completo'), 'Nombre completo', errores)

    username = _texto(form.get('username'), 'Username', errores, minimo=3, maximo=50)
    if username is not None and not _PATRON_USERNAME.match(username):
        errores.append('Username: solo puede contener letras, números, puntos, guiones y guion bajo.')
        username = None
    datos['username'] = username

    datos['password'] = _texto(form.get('password'), 'Contraseña', errores, minimo=6, maximo=100)

    datos['rol'] = _enum(form.get('rol'), 'Rol', {'admin_ti', 'admin_tienda', 'supervisor'}, errores)

    sede_requerida = datos['rol'] == 'admin_tienda'
    sede_valor = (form.get('sede_id') or '').strip()
    if not sede_valor and not sede_requerida:
        datos['sede_id'] = None
    else:
        datos['sede_id'] = _sede_id(form.get('sede_id'), 'Sede', sedes_validas, errores, requerido=sede_requerida)

    datos['activo'] = _enum(form.get('activo'), 'Estado', {'0', '1'}, errores)

    if errores:
        raise ValidationError(errores)
    return datos


def validar_sede(form):
    errores = []
    datos = {}

    datos['nombre'] = _texto(form.get('nombre'), 'Nombre', errores, minimo=2, maximo=100)
    datos['direccion'] = _texto(form.get('direccion'), 'Dirección', errores, minimo=2, maximo=255)

    if errores:
        raise ValidationError(errores)
    return datos


def validar_estado_ticket(valor):
    errores = []
    estado = _enum(valor, 'Estado', {'pendiente', 'en_proceso', 'resuelto'}, errores)
    if errores:
        raise ValidationError(errores)
    return estado


def validar_gestion_solicitud(form):
    errores = []
    datos = {}

    datos['estado'] = _enum(form.get('estado'), 'Estado', {'pendiente', 'aprobado', 'rechazado'}, errores)
    datos['observacion_admin'] = _texto(
        form.get('observacion_admin'), 'Observación', errores, minimo=0, maximo=2000, requerido=False) or ''

    if errores:
        raise ValidationError(errores)
    return datos


def validar_comentario_ticket(valor):
    errores = []
    comentario = _texto(valor, 'Comentario', errores, minimo=1, maximo=2000)
    if errores:
        raise ValidationError(errores)
    return comentario
