-- ==============================================================================
-- PLD Space: Gestión de Unidades y Ensayos MIURA
-- Script Único Completo: Creación de tablas + Inserción de datos iniciales
-- Ejecutar en pgAdmin sobre la base de datos: pldspace_lab
-- ==============================================================================

-- 1. LIMPIEZA DE TABLAS PREVIAS (si existen)
DROP TABLE IF EXISTS unidades CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;

-- 2. TABLA DE USUARIOS (Técnicos e Ingenieros)
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(40) NOT NULL UNIQUE,
    clave VARCHAR(100) NOT NULL
);

-- 3. TABLA DE UNIDADES (Lanzadores y módulos de la familia MIURA)
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

-- 4. INSERCIÓN DE USUARIOS DE PRUEBA
INSERT INTO usuarios (usuario, clave) VALUES
('raul.torres', 'miura2023'),
('pablo.gallego', 'tepida5'),
('ingeniero.control', 'control123');

-- 5. INSERCIÓN DE UNIDADES DE PRUEBA
-- Se incluyen varias unidades con estado distinto a 'EN_ENSAYOS' para las pruebas transaccionales
INSERT INTO unidades (codigo, modelo, estado, responsable_id) VALUES
('M1-AULA01', 'MIURA 1', 'PLANIFICADA', 1),
('M5-AULA01', 'MIURA 5', 'INTEGRACION', 1),
('M5-AULA02', 'MIURA 5', 'INTEGRACION', 2),
('M5-AULA03', 'MIURA 5', 'REVISION', 2),
('M1-SN001',  'MIURA 1', 'EN_ENSAYOS', 3);
