from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

FAQ = {
    # Tickets
    "¿Cómo creo un ticket?": (
        "Ve al menú lateral y haz clic en 'Tickets', luego usa el botón 'Nuevo Ticket'. "
        "Completa el título, descripción, categoría, prioridad y datos del equipo afectado."
    ),
    "¿Qué categorías de ticket existen?": (
        "Las categorías disponibles son: Hardware, Software, Red, Impresoras, Otro."
    ),
    "¿Qué prioridades tiene un ticket?": (
        "Un ticket puede tener prioridad Baja, Media o Alta según la urgencia del problema."
    ),
    "¿Cómo cambio el estado de un ticket?": (
        "Desde la lista de tickets, haz clic en 'Gestionar'. Ahí puedes cambiar el estado "
        "a Pendiente, En proceso o Resuelto, y agregar un comentario de administrador."
    ),
    "¿Puedo editar o eliminar un ticket?": (
        "Sí. Desde la lista de tickets usa los íconos de editar (lápiz) o eliminar (papelera) "
        "en cada fila."
    ),
    "¿Cómo filtro los tickets?": (
        "En la lista de tickets encontrarás filtros por fecha, sede, prioridad, estado y categoría. "
        "Si tu rol es admin de tienda, solo verás los tickets de tu sede."
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
    "¿Cómo gestiono una solicitud de cliente?": (
        "Desde la lista de solicitudes, haz clic en 'Gestionar'. Puedes cambiar el estado "
        "a Pendiente, En proceso o Resuelto, y agregar una observación."
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

    # Sedes
    "¿Cómo agrego una sede?": (
        "En el menú lateral (solo visible para admin_ti) ve a 'Sedes' y usa el botón 'Nueva Sede'. "
        "Ingresa el nombre y dirección."
    ),
    "¿Cómo edito o elimino una sede?": (
        "Desde la lista de sedes usa los íconos de editar o eliminar en cada fila."
    ),

    # Usuarios
    "¿Cómo creo un usuario?": (
        "Ve a 'Usuarios' (solo admin_ti) y haz clic en 'Nuevo Usuario'. "
        "Completa nombre, username, contraseña, rol y sede asignada."
    ),
    "¿Qué roles existen?": (
        "Existen dos roles: 'admin_ti' (acceso completo al sistema) y "
        "'admin_tienda' (acceso limitado a los datos de su propia sede)."
    ),
    "¿Cómo desactivo un usuario?": (
        "Edita el usuario desde la lista y cambia el campo 'Activo' a No."
    ),

    # Sesión
    "¿Cómo cierro sesión?": (
        "Haz clic en el ícono de salida (logout) en la parte inferior del menú lateral."
    ),
    "¿Qué hago si olvidé mi contraseña?": (
        "Contacta al administrador del sistema (admin_ti) para que restablezca tu contraseña."
    ),

    # General
    "¿Qué es el HelpDesk de ElSuper?": (
        "Es el sistema interno de soporte técnico de ElSuper. Permite registrar y gestionar "
        "tickets de TI, solicitudes de clientes y movimientos de equipos por sede."
    ),
    "¿Puedo ver datos de otras sedes?": (
        "Si tu rol es admin_tienda, solo ves los datos de tu propia sede. "
        "El admin_ti tiene visibilidad completa de todas las sedes."
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
