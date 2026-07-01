-- ============================================================
--  HelpDesk - Schema completo
--  Base de datos: railway
--  Generado: 2026-06-23
-- ============================================================

SET FOREIGN_KEY_CHECKS = 0;

-- ------------------------------------------------------------
--  1. sedes
-- ------------------------------------------------------------
CREATE TABLE `sedes` (
  `id`         int          NOT NULL AUTO_INCREMENT,
  `nombre`     varchar(100) NOT NULL,
  `direccion`  varchar(255)     DEFAULT NULL,
  `activo`     tinyint(1)   NOT NULL DEFAULT '1',
  `created_at` datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- ------------------------------------------------------------
--  2. usuarios  (depende de: sedes)
-- ------------------------------------------------------------
CREATE TABLE `usuarios` (
  `id`              int          NOT NULL AUTO_INCREMENT,
  `nombre_completo` varchar(150) NOT NULL,
  `username`        varchar(50)  NOT NULL,
  `password`        varchar(100) NOT NULL,
  `rol`             enum('admin_ti','admin_tienda','supervisor') NOT NULL,
  `sede_id`         int              DEFAULT NULL,
  `activo`          tinyint(1)   NOT NULL DEFAULT '1',
  `created_at`      datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_username` (`username`),
  KEY `fk_usuarios_sede` (`sede_id`),
  CONSTRAINT `fk_usuarios_sede`
    FOREIGN KEY (`sede_id`) REFERENCES `sedes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- ------------------------------------------------------------
--  3. tickets  (depende de: sedes, usuarios)
-- ------------------------------------------------------------
CREATE TABLE `tickets` (
  `id`               int          NOT NULL AUTO_INCREMENT,
  `titulo`           varchar(200) NOT NULL,
  `descripcion`      text         NOT NULL,
  `categoria`        enum('hardware','software','conectividad','otro') NOT NULL,
  `prioridad`        enum('baja','media','alta','critica')             NOT NULL DEFAULT 'media',
  `estado`           enum('pendiente','en_proceso','resuelto')         NOT NULL DEFAULT 'pendiente',
  `comentario_admin` text             DEFAULT NULL,
  `equipo_afectado`  varchar(150)     DEFAULT NULL,
  `cantidad_equipos` tinyint unsigned NOT NULL DEFAULT '1',
  `nombre_contacto`  varchar(150)     DEFAULT NULL,
  `telefono_contacto` varchar(20)     DEFAULT NULL,
  `fecha_limite`     date             DEFAULT NULL,
  `sede_id`          int          NOT NULL,
  `creado_por`       int          NOT NULL,
  `resuelto_por`     int              DEFAULT NULL,
  `resuelto_at`      datetime         DEFAULT NULL,
  `confirmado_por`   int              DEFAULT NULL,
  `confirmado_at`    datetime         DEFAULT NULL,
  `updated_at`       datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_at`       datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_tickets_sede`     (`sede_id`),
  KEY `fk_tickets_creado`   (`creado_por`),
  KEY `fk_tickets_resuelto` (`resuelto_por`),
  KEY `fk_tickets_confirmado` (`confirmado_por`),
  CONSTRAINT `fk_tickets_sede`
    FOREIGN KEY (`sede_id`)      REFERENCES `sedes`    (`id`),
  CONSTRAINT `fk_tickets_creado`
    FOREIGN KEY (`creado_por`)   REFERENCES `usuarios` (`id`),
  CONSTRAINT `fk_tickets_resuelto`
    FOREIGN KEY (`resuelto_por`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `fk_tickets_confirmado`
    FOREIGN KEY (`confirmado_por`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- ------------------------------------------------------------
--  4. solicitudes_cliente  (depende de: sedes, usuarios)
-- ------------------------------------------------------------
CREATE TABLE `solicitudes_cliente` (
  `id`                int          NOT NULL AUTO_INCREMENT,
  `nombre_cliente`    varchar(150) NOT NULL,
  `apellido_cliente`  varchar(150) NOT NULL,
  `tipo_documento`    enum('dni','ce','pasaporte','ruc','ptp','otro') NOT NULL,
  `numero_documento`  varchar(20)  NOT NULL,
  `telefono_cliente`  varchar(20)      DEFAULT NULL,
  `email_cliente`     varchar(150)     DEFAULT NULL,
  `tipo`              enum('alta','baja') NOT NULL,
  `motivo`            text         NOT NULL,
  `estado`            enum('pendiente','aprobado','rechazado') NOT NULL DEFAULT 'pendiente',
  `observacion_admin` text             DEFAULT NULL,
  `sede_id`           int          NOT NULL,
  `solicitado_por`    int          NOT NULL,
  `resuelto_por`      int              DEFAULT NULL,
  `resuelto_at`       datetime         DEFAULT NULL,
  `updated_at`        datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_at`        datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_sol_sede`       (`sede_id`),
  KEY `fk_sol_solicitado` (`solicitado_por`),
  KEY `fk_sol_resuelto`   (`resuelto_por`),
  CONSTRAINT `fk_sol_sede`
    FOREIGN KEY (`sede_id`)        REFERENCES `sedes`    (`id`),
  CONSTRAINT `fk_sol_solicitado`
    FOREIGN KEY (`solicitado_por`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `fk_sol_resuelto`
    FOREIGN KEY (`resuelto_por`)   REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- ------------------------------------------------------------
--  5. movimientos_equipo  (depende de: sedes, usuarios)
-- ------------------------------------------------------------
CREATE TABLE `movimientos_equipo` (
  `id`             int          NOT NULL AUTO_INCREMENT,
  `tipo`           enum('entrada','salida') NOT NULL,
  `tipo_equipo`    varchar(100) NOT NULL,
  `modelo`         varchar(150) NOT NULL,
  `numero_serie`   varchar(100) NOT NULL,
  `sede_id`        int          NOT NULL,
  `responsable`    varchar(150) NOT NULL,
  `fecha`          date         NOT NULL,
  `registrado_por` int          NOT NULL,
  `created_at`     datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_mov_sede`       (`sede_id`),
  KEY `fk_mov_registrado` (`registrado_por`),
  CONSTRAINT `fk_mov_sede`
    FOREIGN KEY (`sede_id`)        REFERENCES `sedes`    (`id`),
  CONSTRAINT `fk_mov_registrado`
    FOREIGN KEY (`registrado_por`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- ------------------------------------------------------------
--  6. trabajadores  (depende de: sedes, usuarios)
-- ------------------------------------------------------------
CREATE TABLE `trabajadores` (
  `id`               int          NOT NULL AUTO_INCREMENT,
  `nombre`           varchar(150) NOT NULL,
  `apellido`         varchar(150) NOT NULL,
  `tipo_documento`   enum('dni','ce','pasaporte','ruc','ptp','otro') NOT NULL,
  `numero_documento` varchar(20)  NOT NULL,
  `telefono`         varchar(20)      DEFAULT NULL,
  `rol`              varchar(100) NOT NULL,
  `fecha_inicio`     date         NOT NULL,
  `fecha_fin`        date             DEFAULT NULL,
  `sede_id`          int          NOT NULL,
  `registrado_por`   int          NOT NULL,
  `updated_at`       datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_at`       datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_trab_sede`       (`sede_id`),
  KEY `fk_trab_registrado` (`registrado_por`),
  CONSTRAINT `fk_trab_sede`
    FOREIGN KEY (`sede_id`)        REFERENCES `sedes`    (`id`),
  CONSTRAINT `fk_trab_registrado`
    FOREIGN KEY (`registrado_por`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


SET FOREIGN_KEY_CHECKS = 1;


-- ============================================================
--  Datos iniciales
-- ============================================================

-- Sedes requeridas por los usuarios de prueba
INSERT INTO `sedes` (`id`, `nombre`, `direccion`) VALUES
  (1, 'Sede Luis Gonzales', 'Av. Luis Gonzales 881, Chiclayo 14001'),
  (9, 'Sede Villa Norte',   'Villa del Norte Mza L Lote 7, Las Ostras');

-- Usuarios (contraseñas en texto plano tal como están en producción)
INSERT INTO `usuarios` (`id`, `nombre_completo`, `username`, `password`, `rol`, `sede_id`, `activo`) VALUES
  (1, 'Administrador TI',  'admin_ti',  'admin123', 'admin_ti',     NULL, 1),
  (2, 'Usuario Prueba',    'usuario',   'usuario',  'admin_tienda',    1, 1),
  (3, 'Usuario Prueba 2',  'usuario2',  'usuario2', 'admin_tienda',    9, 1);

-- Trabajadores de prueba (uno con fecha_fin vencida para ver el indicador)
INSERT INTO `trabajadores`
  (`nombre`, `apellido`, `tipo_documento`, `numero_documento`, `telefono`,
   `rol`, `fecha_inicio`, `fecha_fin`, `sede_id`, `registrado_por`) VALUES
  ('Maria',  'Quispe',   'dni', '45678912', '987654321', 'Cajera',     '2024-01-15', NULL,         1, 2),
  ('Jose',   'Ramirez',  'dni', '41236547', '912345678', 'Supervisor', '2026-01-01', '2026-12-31', 1, 2),
  ('Lucia',  'Fernandez','dni', '47852136', '998877665', 'Vendedora',  '2024-03-10', '2025-03-10', 9, 3);
