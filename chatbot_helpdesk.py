from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


ROL_ADMIN_TI = 'admin_ti'
ROL_ADMIN_TIENDA = 'admin_tienda'
ROL_SUPERVISOR = 'supervisor'
ROLES_GESTION = (ROL_ADMIN_TI, ROL_SUPERVISOR)  # acceso a Sedes/Usuarios/Movimientos de Equipo

# Cada entrada define en que roles aparece ('roles': None = visible para todos).
# 'respuesta' puede ser un texto unico o un dict {rol: texto} con clave
# opcional '_default' para los roles no listados explicitamente.
FAQ = [
    # ---------------------------------------------------------------
    # Tickets
    # ---------------------------------------------------------------
    {
        'pregunta': "¿Cómo creo un ticket?",
        'roles': None,
        'respuesta': (
            "Ve al menú lateral y haz clic en 'Tickets', luego usa el botón 'Nuevo Ticket'. "
            "Completa el título, descripción, categoría, prioridad y datos del equipo afectado."
        ),
    },
    {
        'pregunta': "¿Cómo reporto un problema técnico o falla?",
        'roles': None,
        'respuesta': (
            "Registra un ticket nuevo. Ve a 'Tickets' > 'Nuevo Ticket', describe el problema, "
            "elige la categoría (Hardware, Software, Conectividad u Otro) y la prioridad."
        ),
    },
    {
        'pregunta': "¿Qué datos debo llenar al crear un ticket?",
        'roles': None,
        'respuesta': (
            "Necesitas título, descripción del problema, categoría, prioridad, el equipo afectado, "
            "la cantidad de equipos, y el nombre y teléfono de la persona de contacto."
        ),
    },
    {
        'pregunta': "¿Qué categorías de ticket existen?",
        'roles': None,
        'respuesta': "Las categorías disponibles son: Hardware, Software, Conectividad, Otro.",
    },
    {
        'pregunta': "¿Qué prioridades tiene un ticket?",
        'roles': None,
        'respuesta': "Un ticket puede tener prioridad Baja, Media, Alta o Crítica según la urgencia del problema.",
    },
    {
        'pregunta': "¿Qué prioridad debo elegir para mi ticket?",
        'roles': None,
        'respuesta': (
            "Usa prioridad Crítica o Alta para problemas que detienen la operación, Media para fallas "
            "importantes pero con alternativa, y Baja para incidencias menores o consultas."
        ),
    },
    {
        'pregunta': "¿Qué estados puede tener un ticket?",
        'roles': None,
        'respuesta': (
            "Un ticket puede estar Pendiente (recién creado), En proceso (siendo atendido) "
            "o Resuelto (ya solucionado)."
        ),
    },
    {
        'pregunta': "¿Cómo cambio el estado de un ticket?",
        'roles': None,
        'respuesta': {
            ROL_ADMIN_TIENDA: (
                "Como admin. de tienda no puedes cambiar el estado de un ticket. Puedes abrir "
                "'Gestionar' en el ticket para ver su avance y dejar un comentario; el cambio de "
                "estado lo realiza TI o el supervisor."
            ),
            '_default': (
                "Desde la lista de tickets, haz clic en 'Gestionar'. Ahí puedes cambiar el estado "
                "a Pendiente, En proceso o Resuelto, y agregar un comentario."
            ),
        },
    },
    {
        'pregunta': "¿Cómo atiendo o resuelvo un ticket?",
        'roles': (ROL_ADMIN_TI, ROL_SUPERVISOR),
        'respuesta': (
            "Entra a 'Gestionar' en el ticket, cambia su estado a 'En proceso' mientras lo trabajas "
            "y a 'Resuelto' cuando termines. Puedes dejar un comentario explicando la solución."
        ),
    },
    {
        'pregunta': "¿Cómo confirmo la finalización de un ticket?",
        'roles': (ROL_SUPERVISOR,),
        'respuesta': (
            "Solo el supervisor puede dar el visto bueno final. Entra a 'Gestionar' en un ticket "
            "que ya esté en estado Resuelto y usa el botón de confirmar finalización."
        ),
    },
    {
        'pregunta': "¿Quién da el visto bueno final de un ticket resuelto?",
        'roles': None,
        'respuesta': (
            "El supervisor confirma la finalización de los tickets que ya están en estado Resuelto, "
            "como control de calidad adicional."
        ),
    },
    {
        'pregunta': "¿Cómo agrego un comentario a un ticket?",
        'roles': None,
        'respuesta': (
            "En la pantalla de 'Gestionar' del ticket hay un campo de comentario "
            "donde puedes registrar notas o la solución aplicada. Queda guardado en el historial "
            "con tu nombre, rol y fecha."
        ),
    },
    {
        'pregunta': "¿Cómo veo el detalle de un ticket?",
        'roles': None,
        'respuesta': (
            "Desde la lista de tickets haz clic en 'Gestionar' para ver toda la información del ticket, "
            "incluyendo su estado, sede, contacto e historial de comentarios."
        ),
    },
    {
        'pregunta': "¿Puedo editar o eliminar un ticket?",
        'roles': None,
        'respuesta': (
            "Sí. Desde la lista de tickets usa los íconos de editar (lápiz) o eliminar (papelera) "
            "en cada fila."
        ),
    },
    {
        'pregunta': "¿Cómo edito un ticket ya creado?",
        'roles': None,
        'respuesta': (
            "En la lista de tickets haz clic en el ícono de lápiz (editar) de la fila correspondiente, "
            "modifica los campos y guarda los cambios."
        ),
    },
    {
        'pregunta': "¿Cómo filtro los tickets?",
        'roles': None,
        'respuesta': {
            ROL_ADMIN_TIENDA: (
                "En la lista de tickets encontrarás filtros por fecha, prioridad, estado y categoría. "
                "Como admin. de tienda solo ves los tickets de tu propia sede."
            ),
            '_default': (
                "En la lista de tickets encontrarás filtros por fecha, sede, prioridad, estado y categoría."
            ),
        },
    },
    {
        'pregunta': "¿Para qué sirve el campo equipo afectado y cantidad de equipos?",
        'roles': None,
        'respuesta': (
            "Indican qué equipo presenta la falla (por ejemplo una PC o impresora) y cuántas unidades "
            "están afectadas, para que el área de TI dimensione el problema."
        ),
    },

    # ---------------------------------------------------------------
    # Solicitudes de cliente
    # ---------------------------------------------------------------
    {
        'pregunta': "¿Qué es una solicitud de cliente?",
        'roles': None,
        'respuesta': (
            "Es un registro de alta o baja solicitada por un cliente. Incluye sus datos "
            "personales, tipo de solicitud y motivo."
        ),
    },
    {
        'pregunta': "¿Cómo registro una solicitud de cliente?",
        'roles': None,
        'respuesta': (
            "Ve a 'Solicitudes de Cliente' en el menú lateral y usa el botón 'Nueva Solicitud'. "
            "Ingresa nombre, documento, teléfono, email, tipo y motivo."
        ),
    },
    {
        'pregunta': "¿Qué tipos de solicitud de cliente existen?",
        'roles': None,
        'respuesta': "Una solicitud puede ser de tipo Alta o Baja, según lo que pida el cliente.",
    },
    {
        'pregunta': "¿Qué datos del cliente necesito para registrar una solicitud?",
        'roles': None,
        'respuesta': (
            "Necesitas nombre y apellido, tipo y número de documento, teléfono, email, "
            "el tipo de solicitud y el motivo."
        ),
    },
    {
        'pregunta': "¿Qué tipos de documento puedo registrar para un cliente?",
        'roles': None,
        'respuesta': (
            "Puedes registrar DNI, Carné de Extranjería, Pasaporte, RUC, PTP u Otro, "
            "según corresponda al cliente."
        ),
    },
    {
        'pregunta': "¿Qué estados puede tener una solicitud de cliente?",
        'roles': None,
        'respuesta': "Una solicitud puede estar Pendiente, Aprobada o Rechazada.",
    },
    {
        'pregunta': "¿Cómo gestiono una solicitud de cliente?",
        'roles': None,
        'respuesta': (
            "Desde la lista de solicitudes, haz clic en 'Gestionar'. Puedes cambiar el estado "
            "a Aprobado o Rechazado, y agregar una observación."
        ),
    },
    {
        'pregunta': "¿Cómo agrego una observación a una solicitud?",
        'roles': None,
        'respuesta': (
            "En la pantalla de 'Gestionar' de la solicitud hay un campo de observación del administrador "
            "para dejar notas sobre la atención del caso."
        ),
    },
    {
        'pregunta': "¿Cómo edito o elimino una solicitud de cliente?",
        'roles': None,
        'respuesta': (
            "Desde la lista de solicitudes usa el ícono de lápiz para editar o el de papelera para eliminar "
            "en la fila correspondiente."
        ),
    },
    {
        'pregunta': "¿Cómo filtro o busco solicitudes de cliente?",
        'roles': None,
        'respuesta': {
            ROL_ADMIN_TIENDA: (
                "En la lista de solicitudes puedes filtrar por rango de fechas, tipo y estado. "
                "Como admin. de tienda solo ves las solicitudes de tu propia sede."
            ),
            '_default': (
                "En la lista de solicitudes puedes filtrar por rango de fechas, sede, tipo y estado."
            ),
        },
    },

    # ---------------------------------------------------------------
    # Trabajadores
    # ---------------------------------------------------------------
    {
        'pregunta': "¿Qué es el módulo de trabajadores?",
        'roles': None,
        'respuesta': (
            "Es el registro del personal asignado a cada sede: nombre, documento, teléfono, "
            "rol o cargo, y fecha de inicio/fin del contrato o convenio."
        ),
    },
    {
        'pregunta': "¿Cómo registro un trabajador?",
        'roles': None,
        'respuesta': (
            "Ve a 'Trabajadores' en el menú y usa el botón 'Nuevo Trabajador'. Completa nombre, "
            "apellido, documento, teléfono, rol/cargo, fecha de inicio y, si aplica, fecha de fin."
        ),
    },
    {
        'pregunta': "¿Qué significa que un trabajador esté vencido?",
        'roles': None,
        'respuesta': (
            "Significa que su fecha de fin ya pasó. En la lista y en el dashboard se marca en rojo "
            "como 'Vencido' para que sepas que su contrato o convenio debe revisarse."
        ),
    },
    {
        'pregunta': "¿Qué diferencia hay entre vigente, vencido y sin fecha fin?",
        'roles': None,
        'respuesta': (
            "Vigente: tiene fecha de fin y aún no llega. Vencido: la fecha de fin ya pasó. "
            "Sin fecha fin: no se registró fecha de fin, se asume indefinido."
        ),
    },
    {
        'pregunta': "¿Cómo edito o elimino un trabajador?",
        'roles': None,
        'respuesta': (
            "Desde la lista de trabajadores usa el ícono de editar (lápiz) o eliminar (papelera) "
            "en la fila correspondiente."
        ),
    },
    {
        'pregunta': "¿Cómo filtro la lista de trabajadores?",
        'roles': None,
        'respuesta': (
            "Puedes filtrar por rango de fecha de inicio, rol/cargo y estado "
            "(vigente, vencido o sin fecha fin)."
        ),
    },

    # ---------------------------------------------------------------
    # Movimientos de equipo (solo admin_ti / supervisor)
    # ---------------------------------------------------------------
    {
        'pregunta': "¿Qué es un movimiento de equipo?",
        'roles': ROLES_GESTION,
        'respuesta': (
            "Registra el ingreso o salida de un equipo (computadora, impresora, etc.) en una sede."
        ),
    },
    {
        'pregunta': "¿Cómo registro un movimiento de equipo?",
        'roles': ROLES_GESTION,
        'respuesta': (
            "Ve a 'Movimientos de Equipo' y haz clic en 'Nuevo Movimiento'. "
            "Selecciona tipo (Entrada/Salida), tipo de equipo, modelo, número de serie, sede y responsable."
        ),
    },
    {
        'pregunta': "¿Qué tipos de movimiento de equipo existen?",
        'roles': ROLES_GESTION,
        'respuesta': (
            "Existen dos tipos: Entrada (cuando un equipo llega a una sede) y "
            "Salida (cuando un equipo se retira de una sede)."
        ),
    },
    {
        'pregunta': "¿Qué datos necesito para registrar un movimiento de equipo?",
        'roles': ROLES_GESTION,
        'respuesta': (
            "Necesitas el tipo (Entrada/Salida), el tipo de equipo, el modelo, el número de serie, "
            "la sede, el responsable y la fecha del movimiento."
        ),
    },
    {
        'pregunta': "¿Quién puede ver los movimientos de equipo?",
        'roles': None,
        'respuesta': {
            ROL_ADMIN_TIENDA: (
                "El módulo de Movimientos de Equipo no está disponible para el rol admin. de tienda. "
                "Si necesitas información sobre un movimiento, contacta a TI o a tu supervisor."
            ),
            '_default': (
                "Los roles admin_ti y supervisor pueden registrar, ver y gestionar los movimientos de equipo."
            ),
        },
    },
    {
        'pregunta': "¿Cómo edito o elimino un movimiento de equipo?",
        'roles': ROLES_GESTION,
        'respuesta': (
            "Desde la lista de movimientos usa el ícono de editar (lápiz) o el de eliminar (papelera) "
            "en la fila del movimiento."
        ),
    },
    {
        'pregunta': "¿Cómo filtro los movimientos de equipo?",
        'roles': ROLES_GESTION,
        'respuesta': (
            "En la lista de movimientos puedes filtrar por rango de fechas, sede, tipo y tipo de equipo."
        ),
    },

    # ---------------------------------------------------------------
    # Sedes (solo admin_ti / supervisor)
    # ---------------------------------------------------------------
    {
        'pregunta': "¿Qué es una sede?",
        'roles': None,
        'respuesta': (
            "Una sede es una tienda o local de ElSuper. Los tickets, solicitudes, trabajadores y "
            "movimientos se asocian a una sede para organizarlos."
        ),
    },
    {
        'pregunta': "¿Cómo agrego una sede?",
        'roles': ROLES_GESTION,
        'respuesta': (
            "En el menú lateral ve a 'Sedes' y usa el botón 'Nueva Sede'. "
            "Ingresa el nombre y dirección."
        ),
    },
    {
        'pregunta': "¿Cómo edito o elimino una sede?",
        'roles': ROLES_GESTION,
        'respuesta': "Desde la lista de sedes usa los íconos de editar o eliminar en cada fila.",
    },
    {
        'pregunta': "¿Quién puede administrar las sedes?",
        'roles': None,
        'respuesta': {
            ROL_ADMIN_TIENDA: (
                "Como admin. de tienda no puedes crear, editar ni eliminar sedes; ese módulo lo "
                "gestionan admin_ti y supervisor."
            ),
            '_default': "Los roles admin_ti y supervisor pueden crear, editar o eliminar sedes desde el menú 'Sedes'.",
        },
    },

    # ---------------------------------------------------------------
    # Usuarios (solo admin_ti / supervisor)
    # ---------------------------------------------------------------
    {
        'pregunta': "¿Cómo creo un usuario?",
        'roles': ROLES_GESTION,
        'respuesta': (
            "Ve a 'Usuarios' y haz clic en 'Nuevo Usuario'. "
            "Completa nombre, username, contraseña, rol y sede asignada."
        ),
    },
    {
        'pregunta': "¿Qué datos necesito para crear un usuario?",
        'roles': ROLES_GESTION,
        'respuesta': (
            "Necesitas el nombre completo, el nombre de usuario (username), una contraseña, "
            "el rol (admin_ti, admin_tienda o supervisor), la sede asignada y si estará activo."
        ),
    },
    {
        'pregunta': "¿Qué roles existen?",
        'roles': None,
        'respuesta': (
            "Existen tres roles: 'admin_ti' (acceso completo al sistema), 'supervisor' (visibilidad "
            "de toda la red y confirma la finalización de tickets) y 'admin_tienda' (acceso limitado "
            "a los datos de su propia sede)."
        ),
    },
    {
        'pregunta': "¿Cuál es la diferencia entre admin_ti, supervisor y admin_tienda?",
        'roles': None,
        'respuesta': (
            "admin_ti: gestiona todo el sistema, todas las sedes, usuarios, sedes y movimientos de equipo. "
            "supervisor: tiene la misma visibilidad de toda la red y además confirma la finalización de "
            "los tickets resueltos. admin_tienda: solo ve y gestiona los datos de su propia sede y no "
            "puede cambiar el estado de los tickets."
        ),
    },
    {
        'pregunta': "¿Cómo edito un usuario?",
        'roles': ROLES_GESTION,
        'respuesta': (
            "Ve a 'Usuarios', haz clic en el ícono de editar (lápiz) del usuario, "
            "cambia los datos necesarios y guarda."
        ),
    },
    {
        'pregunta': "¿Cómo desactivo un usuario?",
        'roles': ROLES_GESTION,
        'respuesta': "Edita el usuario desde la lista y cambia el campo 'Activo' a No.",
    },
    {
        'pregunta': "¿Cómo elimino un usuario?",
        'roles': ROLES_GESTION,
        'respuesta': (
            "Desde la lista de usuarios usa el ícono de papelera (eliminar) en la fila del usuario. "
            "También puedes solo desactivarlo si prefieres conservar su historial."
        ),
    },
    {
        'pregunta': "¿Cómo cambio el rol o la sede de un usuario?",
        'roles': ROLES_GESTION,
        'respuesta': "Edita el usuario desde 'Usuarios' y actualiza los campos de rol y sede asignada, luego guarda.",
    },
    {
        'pregunta': "¿Cómo filtro la lista de usuarios?",
        'roles': ROLES_GESTION,
        'respuesta': "En la lista de usuarios puedes filtrar por sede, rol y estado (activo o inactivo).",
    },

    # ---------------------------------------------------------------
    # Reportes / exportación
    # ---------------------------------------------------------------
    {
        'pregunta': "¿Cómo exporto un reporte?",
        'roles': None,
        'respuesta': (
            "En la parte superior de las listas de Tickets, Solicitudes de Cliente, Trabajadores y "
            "Movimientos de Equipo hay botones 'CSV' y 'PDF' que exportan los registros aplicando los "
            "filtros que tengas seleccionados."
        ),
    },
    {
        'pregunta': "¿Puedo descargar los tickets en PDF o Excel?",
        'roles': None,
        'respuesta': (
            "Sí. En la lista de tickets usa el botón 'PDF' para un reporte imprimible o 'CSV' para "
            "abrirlo en Excel."
        ),
    },

    # ---------------------------------------------------------------
    # Sesión y acceso
    # ---------------------------------------------------------------
    {
        'pregunta': "¿Cómo inicio sesión?",
        'roles': None,
        'respuesta': (
            "En la pantalla de login ingresa tu nombre de usuario y contraseña, y haz clic en entrar. "
            "Si los datos son correctos llegarás al panel principal."
        ),
    },
    {
        'pregunta': "¿Cómo cierro sesión?",
        'roles': None,
        'respuesta': "Haz clic en el ícono de salida (logout) en la parte inferior del menú lateral.",
    },
    {
        'pregunta': "¿Qué hago si olvidé mi contraseña?",
        'roles': None,
        'respuesta': "Contacta al administrador del sistema (admin_ti) para que restablezca tu contraseña.",
    },
    {
        'pregunta': "¿Por qué no puedo iniciar sesión?",
        'roles': None,
        'respuesta': (
            "Verifica que tu usuario y contraseña sean correctos. Si el problema persiste o tu cuenta "
            "está inactiva, contacta al administrador del sistema (admin_ti)."
        ),
    },
    {
        'pregunta': "¿Cómo cambio mi contraseña?",
        'roles': None,
        'respuesta': (
            "Por seguridad, el cambio de contraseña lo realiza un usuario admin_ti o supervisor "
            "editando tu usuario. Solicítaselo para que la actualice."
        ),
    },

    # ---------------------------------------------------------------
    # Navegación y panel
    # ---------------------------------------------------------------
    {
        'pregunta': "¿Qué puedo hacer en el dashboard?",
        'roles': None,
        'respuesta': {
            ROL_ADMIN_TIENDA: (
                "El panel principal muestra las métricas de tu propia sede: tickets y solicitudes "
                "por estado, trabajadores registrados y tus tickets más recientes. Haz clic en 'Inicio' "
                "en el menú lateral para volver aquí en cualquier momento."
            ),
            '_default': (
                "El panel principal muestra métricas de toda la red: tickets y solicitudes por estado, "
                "trabajadores, sedes activas, usuarios activos, movimientos de equipo del último mes y "
                "los tickets más recientes. Haz clic en 'Inicio' en el menú lateral para volver aquí."
            ),
        },
    },
    {
        'pregunta': "¿Cómo regreso al dashboard o panel principal?",
        'roles': None,
        'respuesta': (
            "Haz clic en la opción 'Inicio' en la parte superior del menú lateral, disponible desde "
            "cualquier pantalla del sistema."
        ),
    },
    {
        'pregunta': "¿Cómo navego por el sistema?",
        'roles': None,
        'respuesta': (
            "Usa el menú lateral para moverte entre las secciones. Las opciones disponibles dependen "
            "de tu rol: el admin_tienda ve menos secciones que admin_ti y supervisor."
        ),
    },
    {
        'pregunta': "¿Cómo funciona la paginación de las listas?",
        'roles': None,
        'respuesta': (
            "Las listas muestran 20 registros por página. Usa los controles de paginación al final "
            "de la lista para avanzar o retroceder entre páginas."
        ),
    },

    # ---------------------------------------------------------------
    # General
    # ---------------------------------------------------------------
    {
        'pregunta': "¿Qué es el HelpDesk de ElSuper?",
        'roles': None,
        'respuesta': (
            "Es el sistema interno de soporte técnico de ElSuper. Permite registrar y gestionar "
            "tickets de TI, solicitudes de clientes, trabajadores y movimientos de equipos por sede."
        ),
    },
    {
        'pregunta': "¿Para qué sirve este sistema?",
        'roles': None,
        'respuesta': (
            "Sirve para centralizar el soporte de ElSuper: reportar y dar seguimiento a fallas de TI, "
            "atender solicitudes de clientes, llevar el registro de trabajadores por sede y controlar "
            "el movimiento de equipos entre sedes."
        ),
    },
    {
        'pregunta': "¿Puedo ver datos de otras sedes?",
        'roles': None,
        'respuesta': {
            ROL_ADMIN_TIENDA: "No. Como admin. de tienda solo ves los datos de tu propia sede.",
            '_default': "Sí, tu rol tiene visibilidad completa de todas las sedes del sistema.",
        },
    },
    {
        'pregunta': "¿Por qué no veo algunas opciones del menú?",
        'roles': None,
        'respuesta': {
            ROL_ADMIN_TIENDA: (
                "El menú se adapta a tu rol. Movimientos de Equipo, Sedes y Usuarios solo están "
                "disponibles para admin_ti y supervisor."
            ),
            '_default': "Si te falta una opción, verifica que tu usuario tenga el rol correcto asignado.",
        },
    },
    {
        'pregunta': "¿Con quién me contacto si tengo un problema con el sistema?",
        'roles': None,
        'respuesta': (
            "Para problemas de acceso, permisos o errores del sistema contacta al administrador "
            "de TI (admin_ti), que puede ayudarte y revisar tu cuenta."
        ),
    },
    {
        'pregunta': "¿Qué hago si me aparece un error en el sistema?",
        'roles': None,
        'respuesta': (
            "Si ves un error, vuelve a intentar la acción. Si continúa, anota qué estabas haciendo "
            "y repórtalo al administrador de TI (admin_ti) para que lo revise."
        ),
    },
    {
        'pregunta': "¿Mis datos y registros se guardan?",
        'roles': None,
        'respuesta': (
            "Sí. Tickets, solicitudes, trabajadores, movimientos, sedes y usuarios se almacenan en la "
            "base de datos del sistema y quedan disponibles para consultarlos y gestionarlos después."
        ),
    },
    {
        'pregunta': "¿Cómo registro una venta?",
        'roles': None,
        'respuesta': "Esto no es un sistema de ventas.",
    },
]


def _resolver_respuesta(respuesta, rol):
    if isinstance(respuesta, dict):
        return respuesta.get(rol, respuesta.get('_default', ''))
    return respuesta


def _construir_indice(rol):
    entradas = [f for f in FAQ if f['roles'] is None or rol in f['roles']]
    preguntas = [f['pregunta'] for f in entradas]
    respuestas = [_resolver_respuesta(f['respuesta'], rol) for f in entradas]
    vectorizer = TfidfVectorizer()
    matriz = vectorizer.fit_transform(preguntas)
    return preguntas, respuestas, vectorizer, matriz


# Un indice TF-IDF distinto por rol para que cada uno solo pueda "encontrar"
# (y recibir) las preguntas/respuestas habilitadas para su propio rol.
_ROLES_CONOCIDOS = (ROL_ADMIN_TI, ROL_ADMIN_TIENDA, ROL_SUPERVISOR)
_INDICE_POR_ROL = {rol: _construir_indice(rol) for rol in _ROLES_CONOCIDOS}
_INDICE_POR_ROL[None] = _construir_indice(None)  # fallback: solo preguntas publicas (roles=None)


def encontrar_respuesta(pregunta_usuario, rol=None, umbral=0.25):
    _preguntas, _respuestas, _vectorizer, _matriz = _INDICE_POR_ROL.get(rol, _INDICE_POR_ROL[None])

    vector_usuario = _vectorizer.transform([pregunta_usuario])
    similitudes = cosine_similarity(vector_usuario, _matriz)[0]
    indice_mejor = np.argmax(similitudes)

    if similitudes[indice_mejor] >= umbral:
        return _respuestas[indice_mejor]
    return "No encontré una respuesta para eso. Intenta preguntar de otra forma o contacta al administrador del sistema."
