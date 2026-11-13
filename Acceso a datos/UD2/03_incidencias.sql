-- ==============================================================
-- UP 2 - SESIÓN 5: TABLAS RELACIONADAS Y CLAVES AUTOGENERADAS
-- Script para crear la tabla 'incidencias' en mutxamel_pg
-- ==============================================================

CREATE TABLE IF NOT EXISTS incidencias (
    id SERIAL PRIMARY KEY,
    software_codigo INTEGER NOT NULL REFERENCES software_auditado(codigo),
    descripcion VARCHAR(150) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
