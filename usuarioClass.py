class Usuario:

    def __init__(self, nombre_completo, username, password, rol, sede_id, activo, id=None):
        self.nombre_completo = nombre_completo
        self.username        = username
        self.password        = password
        self.rol             = rol
        self.sede_id         = sede_id
        self.activo          = activo
        self.id              = id
