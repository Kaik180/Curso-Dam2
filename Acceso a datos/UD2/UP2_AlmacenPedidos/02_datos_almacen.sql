-- ==============================================================
-- PROYECTO UP2: ACCESO A BBDD RELACIONALES (UP2_AlmacenPedidos)
-- Script 02: Datos iniciales de inventario
-- ==============================================================

INSERT INTO Inventario (stock, idProducto) VALUES
(50, 1), -- Producto 1: Stock suficiente para pedido y envío exitoso (ej. pedir 10 -> quedan 40 >= 10)
(15, 2), -- Producto 2: Para probar regla de stock restante < 10 (ej. pedir 8 -> quedan 7 < 10 -> ROLLBACK)
(5,  3), -- Producto 3: Para probar stock insuficiente (ej. pedir 10 -> 5 < 10 -> No se puede realizar)
(25, 4); -- Producto 4: Stock para pruebas generales
