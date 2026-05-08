class Ticket:

    def __init__(self, titulo, descripcion, categoria, prioridad,
                 equipo_afectado, cantidad_equipos,
                 nombre_contacto, telefono_contacto,
                 sede_id, creado_por):
        self.titulo            = titulo
        self.descripcion       = descripcion
        self.categoria         = categoria
        self.prioridad         = prioridad
        self.equipo_afectado   = equipo_afectado
        self.cantidad_equipos  = cantidad_equipos
        self.nombre_contacto   = nombre_contacto
        self.telefono_contacto = telefono_contacto
        self.sede_id           = sede_id
        self.creado_por        = creado_por
