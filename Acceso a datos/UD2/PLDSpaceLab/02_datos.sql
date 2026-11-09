-- ==============================================================
-- PRACTICA - PLD Space: gestión de unidades y ensayos MIURA
-- Script 02: Inserción de datos iniciales
-- Base de datos: pldspace_lab
-- ==============================================================

-- 1. Inserción de usuarios técnicos
-- Nota: En un entorno de producción las contraseñas estarían hasheadas (bcrypt). Para este ejercicio académico se almacenan las claves indicadas.
INSERT INTO usuarios (usuario, clave) VALUES
('raul.torres', 'miura2023'),
('pablo.gallego', 'tepida5'),
('ingeniero.control', 'control123');

-- 2. Inserción de unidades de prueba y desarrollo
-- Aseguramos al menos 2 unidades con estado distinto de 'EN_ENSAYOS' para las pruebas transaccionales
INSERT INTO unidades (codigo, modelo, estado, responsable_id) VALUES
('M1-AULA01', 'MIURA 1', 'PLANIFICADA', 1),
('M5-AULA01', 'MIURA 5', 'INTEGRACION', 1),
('M5-AULA02', 'MIURA 5', 'INTEGRACION', 2),
('M5-AULA03', 'MIURA 5', 'REVISION', 2),
('M1-SN001',  'MIURA 1', 'EN_ENSAYOS', 3);
