-- ==============================================================
-- PRACTICA - PLD Space: gestión de unidades y ensayos MIURA
-- Script 01: Creación del esquema y restricciones de tablas
-- Base de datos: pldspace_lab
-- ==============================================================

-- Eliminar tablas si existen en orden inverso por dependencias
DROP TABLE IF EXISTS unidades CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;

-- 1. Tabla de usuarios (personal técnico y de ingeniería)
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(40) NOT NULL UNIQUE,
    clave VARCHAR(100) NOT NULL
);

-- 2. Tabla de unidades (lanzadores y módulos de la familia MIURA)
CREATE TABLE unidades (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    modelo VARCHAR(20) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    responsable_id INTEGER NOT NULL,
    CONSTRAINT fk_unidades_usuario FOREIGN KEY (responsable_id) REFERENCES usuarios(id) ON DELETE RESTRICT,
    CONSTRAINT chk_unidades_modelo CHECK (modelo IN ('MIURA 1', 'MIURA 5')),
    CONSTRAINT chk_unidades_estado CHECK (estado IN ('PLANIFICADA', 'INTEGRACION', 'EN_ENSAYOS', 'REVISION'))
);
