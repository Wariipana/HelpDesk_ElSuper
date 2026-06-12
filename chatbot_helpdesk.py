from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


FAQ = {
    # Tickets
    "¿Cómo creo un ticket?": (
        "Ve al menú lateral y haz clic en 'Tickets', luego usa el botón 'Nuevo Ticket'. "
        "Completa el título, descripción, categoría, prioridad y datos del equipo afectado."
    ),
    "¿Cómo reporto un problema técnico o falla?": (
        "Registra un ticket nuevo. Ve a 'Tickets' > 'Nuevo Ticket', describe el problema, "
        "elige la categoría (Hardware, Software, Red, Impresoras u Otro) y la prioridad."
    ),
    "¿Qué datos debo llenar al crear un ticket?": (
        "Necesitas título, descripción del problema, categoría, prioridad, el equipo afectado, "
        "la cantidad de equipos, y el nombre y teléfono de la persona de contacto."
    ),
    "¿Qué categorías de ticket existen?": (
        "Las categorías disponibles son: Hardware, Software, Red, Impresoras, Otro."
    ),
    "¿Qué prioridades tiene un ticket?": (
        "Un ticket puede tener prioridad Baja, Media o Alta según la urgencia del problema."
    ),
    "¿Qué prioridad debo elegir para mi ticket?": (
        "Usa prioridad Alta para problemas que detienen la operación, Media para fallas importantes "
        "pero con alternativa, y Baja para incidencias menores o consultas."
    ),
    "¿Qué estados puede tener un ticket?": (
        "Un ticket puede estar Pendiente (recién creado), En proceso (siendo atendido) "
        "o Resuelto (ya solucionado)."
    ),
    "¿Cómo cambio el estado de un ticket?": (
        "Desde la lista de tickets, haz clic en 'Gestionar'. Ahí puedes cambiar el estado "
        "a Pendiente, En proceso o Resuelto, y agregar un comentario de administrador."
    ),
    "¿Cómo atiendo o resuelvo un ticket?": (
        "Entra a 'Gestionar' en el ticket, cambia su estado a 'En proceso' mientras lo trabajas "
        "y a 'Resuelto' cuando termines. Puedes dejar un comentario explicando la solución."
    ),
    "¿Cómo agrego un comentario a un ticket?": (
        "En la pantalla de 'Gestionar' del ticket hay un campo de comentario de administrador "
        "donde puedes registrar notas o la solución aplicada."
    ),
    "¿Cómo veo el detalle de un ticket?": (
        "Desde la lista de tickets haz clic en 'Gestionar' para ver toda la información del ticket, "
        "incluyendo su estado, sede, contacto y comentarios."
    ),
    "¿Puedo editar o eliminar un ticket?": (
        "Sí. Desde la lista de tickets usa los íconos de editar (lápiz) o eliminar (papelera) "
        "en cada fila."
    ),
    "¿Cómo edito un ticket ya creado?": (
        "En la lista de tickets haz clic en el ícono de lápiz (editar) de la fila correspondiente, "
        "modifica los campos y guarda los cambios."
    ),
    "¿Cómo filtro los tickets?": (
        "En la lista de tickets encontrarás filtros por fecha, sede, prioridad, estado y categoría. "
        "Si tu rol es admin de tienda, solo verás los tickets de tu sede."
    ),
    "¿Cómo busco un ticket específico?": (
        "Usa los filtros de la lista de tickets (rango de fechas, sede, prioridad, estado o categoría) "
        "para acotar los resultados y encontrar el ticket que buscas."
    ),
    "¿Para qué sirve el campo equipo afectado y cantidad de equipos?": (
        "Indican qué equipo presenta la falla (por ejemplo una PC o impresora) y cuántas unidades "
        "están afectadas, para que el área de TI dimensione el problema."
    ),

    # Solicitudes de cliente
    "¿Qué es una solicitud de cliente?": (
        "Es un registro de reclamo, consulta o sugerencia de un cliente. Incluye sus datos "
        "personales, tipo de solicitud y motivo."
    ),
    "¿Cómo registro una solicitud de cliente?": (
        "Ve a 'Solicitudes de Cliente' en el menú y usa el botón 'Nueva Solicitud'. "
        "Ingresa nombre, documento, teléfono, email, tipo y motivo."
    ),
    "¿Cómo registro un reclamo o queja de un cliente?": (
        "Ve a 'Solicitudes de Cliente' > 'Nueva Solicitud', completa los datos del cliente, "
        "elige el tipo (por ejemplo reclamo) y describe el motivo."
    ),
    "¿Qué tipos de solicitud de cliente existen?": (
        "Una solicitud puede ser un reclamo, una consulta o una sugerencia, según el motivo del cliente."
    ),
    "¿Qué datos del cliente necesito para registrar una solicitud?": (
        "Necesitas nombre y apellido, tipo y número de documento, teléfono, email, "
        "el tipo de solicitud y el motivo."
    ),
    "¿Qué tipos de documento puedo registrar para un cliente?": (
        "Puedes registrar documentos como DNI, Carné de Extranjería, Pasaporte o RUC, "
        "según corresponda al cliente."
    ),
    "¿Cómo gestiono una solicitud de cliente?": (
        "Desde la lista de solicitudes, haz clic en 'Gestionar'. Puedes cambiar el estado "
        "a Pendiente, En proceso o Resuelto, y agregar una observación."
    ),
    "¿Cómo agrego una observación a una solicitud?": (
        "En la pantalla de 'Gestionar' de la solicitud hay un campo de observación del administrador "
        "para dejar notas sobre la atención del caso."
    ),
    "¿Cómo edito o elimino una solicitud de cliente?": (
        "Desde la lista de solicitudes usa el ícono de lápiz para editar o el de papelera para eliminar "
        "en la fila correspondiente."
    ),
    "¿Cómo filtro o busco solicitudes de cliente?": (
        "En la lista de solicitudes puedes filtrar por rango de fechas, sede, tipo y estado. "
        "Si eres admin_tienda solo verás las de tu sede."
    ),

    # Movimientos de equipo
    "¿Qué es un movimiento de equipo?": (
        "Registra el ingreso o salida de un equipo (computadora, impresora, etc.) en una sede. "
        "Solo el rol admin_ti puede verlo y gestionarlo."
    ),
    "¿Cómo registro un movimiento de equipo?": (
        "Ve a 'Movimientos de Equipo' y haz clic en 'Nuevo Movimiento'. "
        "Selecciona tipo (Ingreso/Salida), tipo de equipo, modelo, número de serie, sede y responsable."
    ),
    "¿Cómo registro el ingreso o la salida de un equipo?": (
        "En 'Movimientos de Equipo' > 'Nuevo Movimiento' elige el tipo Ingreso o Salida, "
        "indica el equipo, modelo, número de serie, sede, responsable y fecha."
    ),
    "¿Qué tipos de movimiento de equipo existen?": (
        "Existen dos tipos: Ingreso (cuando un equipo llega a una sede) y "
        "Salida (cuando un equipo se retira de una sede)."
    ),
    "¿Qué datos necesito para registrar un movimiento de equipo?": (
        "Necesitas el tipo (Ingreso/Salida), el tipo de equipo, el modelo, el número de serie, "
        "la sede, el responsable y la fecha del movimiento."
    ),
    "¿Quién puede ver los movimientos de equipo?": (
        "Solo los usuarios con rol admin_ti pueden registrar, ver y gestionar los movimientos de equipo."
    ),
    "¿Cómo edito o elimino un movimiento de equipo?": (
        "Desde la lista de movimientos usa el ícono de editar (lápiz) o el de eliminar (papelera) "
        "en la fila del movimiento."
    ),
    "¿Cómo filtro los movimientos de equipo?": (
        "En la lista de movimientos puedes filtrar por rango de fechas, sede, tipo y tipo de equipo."
    ),

    # Sedes
    "¿Qué es una sede?": (
        "Una sede es una tienda o local de ElSuper. Los tickets, solicitudes y movimientos "
        "se asocian a una sede para organizarlos."
    ),
    "¿Cómo agrego una sede?": (
        "En el menú lateral (solo visible para admin_ti) ve a 'Sedes' y usa el botón 'Nueva Sede'. "
        "Ingresa el nombre y dirección."
    ),
    "¿Cómo edito o elimino una sede?": (
        "Desde la lista de sedes usa los íconos de editar o eliminar en cada fila."
    ),
    "¿Quién puede administrar las sedes?": (
        "Solo el rol admin_ti puede crear, editar o eliminar sedes desde el menú 'Sedes'."
    ),

    # Usuarios
    "¿Cómo creo un usuario?": (
        "Ve a 'Usuarios' (solo admin_ti) y haz clic en 'Nuevo Usuario'. "
        "Completa nombre, username, contraseña, rol y sede asignada."
    ),
    "¿Qué datos necesito para crear un usuario?": (
        "Necesitas el nombre completo, el nombre de usuario (username), una contraseña, "
        "el rol (admin_ti o admin_tienda), la sede asignada y si estará activo."
    ),
    "¿Qué roles existen?": (
        "Existen dos roles: 'admin_ti' (acceso completo al sistema) y "
        "'admin_tienda' (acceso limitado a los datos de su propia sede)."
    ),
    "¿Cuál es la diferencia entre admin_ti y admin_tienda?": (
        "El admin_ti gestiona todo el sistema y todas las sedes, incluyendo usuarios, sedes y "
        "movimientos de equipo. El admin_tienda solo ve y gestiona los datos de su propia sede."
    ),
    "¿Cómo edito un usuario?": (
        "Ve a 'Usuarios', haz clic en el ícono de editar (lápiz) del usuario, "
        "cambia los datos necesarios y guarda."
    ),
    "¿Cómo desactivo un usuario?": (
        "Edita el usuario desde la lista y cambia el campo 'Activo' a No."
    ),
    "¿Cómo elimino un usuario?": (
        "Desde la lista de usuarios usa el ícono de papelera (eliminar) en la fila del usuario. "
        "También puedes solo desactivarlo si prefieres conservar su historial."
    ),
    "¿Cómo cambio el rol o la sede de un usuario?": (
        "Edita el usuario desde 'Usuarios' y actualiza los campos de rol y sede asignada, luego guarda."
    ),
    "¿Cómo filtro la lista de usuarios?": (
        "En la lista de usuarios puedes filtrar por sede, rol y estado (activo o inactivo)."
    ),

    # Sesión y acceso
    "¿Cómo inicio sesión?": (
        "En la pantalla de login ingresa tu nombre de usuario y contraseña, y haz clic en entrar. "
        "Si los datos son correctos llegarás al panel principal."
    ),
    "¿Cómo cierro sesión?": (
        "Haz clic en el ícono de salida (logout) en la parte inferior del menú lateral."
    ),
    "¿Qué hago si olvidé mi contraseña?": (
        "Contacta al administrador del sistema (admin_ti) para que restablezca tu contraseña."
    ),
    "¿Por qué no puedo iniciar sesión?": (
        "Verifica que tu usuario y contraseña sean correctos. Si el problema persiste o tu cuenta "
        "está inactiva, contacta al administrador del sistema (admin_ti)."
    ),
    "¿Cómo cambio mi contraseña?": (
        "Por seguridad, el cambio de contraseña lo realiza el administrador (admin_ti) "
        "editando tu usuario. Solicítaselo para que la actualice."
    ),

    # Navegación y panel
    "¿Qué puedo hacer en el dashboard?": (
        "El panel principal (dashboard) es la pantalla de inicio tras iniciar sesión. Desde el menú "
        "lateral accedes a tickets, solicitudes de cliente, movimientos de equipo, sedes y usuarios."
    ),
    "¿Cómo navego por el sistema?": (
        "Usa el menú lateral para moverte entre las secciones. Las opciones disponibles dependen "
        "de tu rol: el admin_tienda ve menos secciones que el admin_ti."
    ),
    "¿Cómo funciona la paginación de las listas?": (
        "Las listas muestran 20 registros por página. Usa los controles de paginación al final "
        "de la lista para avanzar o retroceder entre páginas."
    ),

    # General
    "¿Qué es el HelpDesk de ElSuper?": (
        "Es el sistema interno de soporte técnico de ElSuper. Permite registrar y gestionar "
        "tickets de TI, solicitudes de clientes y movimientos de equipos por sede."
    ),
    "¿Para qué sirve este sistema?": (
        "Sirve para centralizar el soporte de ElSuper: reportar y dar seguimiento a fallas de TI, "
        "atender reclamos y consultas de clientes, y controlar el movimiento de equipos entre sedes."
    ),
    "¿Puedo ver datos de otras sedes?": (
        "Si tu rol es admin_tienda, solo ves los datos de tu propia sede. "
        "El admin_ti tiene visibilidad completa de todas las sedes."
    ),
    "¿Por qué no veo algunas opciones del menú?": (
        "El menú se adapta a tu rol. Secciones como Sedes, Usuarios y Movimientos de Equipo "
        "solo están disponibles para el rol admin_ti."
    ),
    "¿Con quién me contacto si tengo un problema con el sistema?": (
        "Para problemas de acceso, permisos o errores del sistema contacta al administrador "
        "de TI (admin_ti), que puede ayudarte y revisar tu cuenta."
    ),
    "¿Qué hago si me aparece un error en el sistema?": (
        "Si ves un error, vuelve a intentar la acción. Si continúa, anota qué estabas haciendo "
        "y repórtalo al administrador de TI (admin_ti) para que lo revise."
    ),
    "¿Mis datos y registros se guardan?": (
        "Sí. Tickets, solicitudes, movimientos, sedes y usuarios se almacenan en la base de datos "
        "del sistema y quedan disponibles para consultarlos y gestionarlos después."
    ),
    "¿Cómo registro una venta?": (
        "Esto no es un sistema de ventas"
    ),
}


_preguntas = list(FAQ.keys())
_respuestas = list(FAQ.values())

_vectorizer = TfidfVectorizer()
_matriz_faq = _vectorizer.fit_transform(_preguntas)


def encontrar_respuesta(pregunta_usuario, umbral=0.25):
    vector_usuario = _vectorizer.transform([pregunta_usuario])
    similitudes = cosine_similarity(vector_usuario, _matriz_faq)[0]
    indice_mejor = np.argmax(similitudes)

    if similitudes[indice_mejor] >= umbral:
        return _respuestas[indice_mejor]
    return "No encontré una respuesta para eso. Intenta preguntar de otra forma o contacta al administrador del sistema."
