-- ==============================================================
-- PROYECTO: Mutxamel Sec-Ops S.L. (mutxamelUP2)
-- Base de datos: mutxamel_pg
-- Esquema completo de tablas
-- ==============================================================

CREATE TABLE IF NOT EXISTS login (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS software_auditado (
    codigo SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    nivel_exposicion INTEGER
);

CREATE TABLE IF NOT EXISTS incidencias (
    id SERIAL PRIMARY KEY,
    software_codigo INTEGER NOT NULL REFERENCES software_auditado(codigo),
    descripcion VARCHAR(150) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
