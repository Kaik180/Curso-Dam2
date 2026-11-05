

-- Tabla: usuarios
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(40) NOT NULL UNIQUE,
    clave VARCHAR(100) NOT NULL
);

-- Tabla: unidades
CREATE TABLE unidades (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    modelo VARCHAR(20) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    responsable_id INTEGER NOT NULL,
    CONSTRAINT fk_unidades_usuario FOREIGN KEY (responsable_id) 
        REFERENCES usuarios(id)
);