class SolicitudCliente:

    def __init__(self, nombre_cliente, apellido_cliente,
                 tipo_documento, numero_documento,
                 telefono_cliente, email_cliente,
                 tipo, motivo, sede_id, solicitado_por):
        self.nombre_cliente    = nombre_cliente
        self.apellido_cliente  = apellido_cliente
        self.tipo_documento    = tipo_documento
        self.numero_documento  = numero_documento
        self.telefono_cliente  = telefono_cliente
        self.email_cliente     = email_cliente
        self.tipo              = tipo
        self.motivo            = motivo
        self.sede_id           = sede_id
        self.solicitado_por    = solicitado_por
