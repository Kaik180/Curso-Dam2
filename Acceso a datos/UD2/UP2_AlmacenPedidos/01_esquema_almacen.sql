-- ==============================================================
-- PROYECTO UP2: ACCESO A BBDD RELACIONALES (UP2_AlmacenPedidos)
-- Script 01: Creación de tablas
-- ==============================================================

DROP TABLE IF EXISTS Envio CASCADE;
DROP TABLE IF EXISTS Pedido CASCADE;
DROP TABLE IF EXISTS Inventario CASCADE;

-- Tabla Inventario: idProducto con restricción UNIQUE
CREATE TABLE Inventario (
    idInventario SERIAL PRIMARY KEY,
    stock INT NOT NULL,
    idProducto INT NOT NULL UNIQUE
);

-- Tabla Pedido: idPedido autoincremental
CREATE TABLE Pedido (
    idPedido SERIAL PRIMARY KEY,
    idCliente INT NOT NULL,
    fecha DATE NOT NULL,
    status VARCHAR(45) NOT NULL,
    idProducto INT NOT NULL,
    cantidad INT NOT NULL
);

-- Tabla Envio: idEnvio autoincremental
CREATE TABLE Envio (
    idEnvio SERIAL PRIMARY KEY,
    fechaEnvio DATE NOT NULL,
    idProducto INT NOT NULL
);
