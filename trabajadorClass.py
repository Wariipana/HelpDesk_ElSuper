class Trabajador:

    def __init__(self, nombre, apellido,
                 tipo_documento, numero_documento,
                 telefono, rol,
                 fecha_inicio, fecha_fin,
                 sede_id, registrado_por, id=None):
        self.nombre           = nombre
        self.apellido         = apellido
        self.tipo_documento   = tipo_documento
        self.numero_documento = numero_documento
        self.telefono         = telefono
        self.rol              = rol
        self.fecha_inicio     = fecha_inicio
        self.fecha_fin        = fecha_fin
        self.sede_id          = sede_id
        self.registrado_por   = registrado_por
        self.id               = id
