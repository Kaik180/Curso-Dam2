DROP TABLE IF EXISTS unidades CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(40) NOT NULL UNIQUE,
    clave VARCHAR(100) NOT NULL
);

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

INSERT INTO usuarios (usuario, clave) VALUES
('raul.torres', 'miura2023'),
('pablo.gallego', 'tepida5'),
('ingeniero.control', 'control123');

INSERT INTO unidades (codigo, modelo, estado, responsable_id) VALUES
('M1-AULA01', 'MIURA 1', 'PLANIFICADA', 1),
('M5-AULA01', 'MIURA 5', 'INTEGRACION', 1),
('M5-AULA02', 'MIURA 5', 'INTEGRACION', 2),
('M5-AULA03', 'MIURA 5', 'REVISION', 2),
('M1-SN001',  'MIURA 1', 'EN_ENSAYOS', 3);
