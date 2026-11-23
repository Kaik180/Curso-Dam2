# Proyecto UP2: Acceso a BBDD Relacionales (UP2_AlmacenPedidos)

**Módulo:** Acceso a Datos (2.º DAM)  
**Curso:** 2026/2027  
**Nombre del Proyecto Maven:** `UP2_AlmacenPedidos`  

---

## 📋 1. Descripción del Proyecto

Sistema de gestión de pedidos y almacén desarrollado en Java con JDBC y PostgreSQL.
Cada vez que se registra un pedido:
1. Se valida la existencia y stock del producto en la tabla `Inventario`.
2. Se procesa el pedido dentro de una **única transacción** con `setAutoCommit(false)`:
   - Se inserta el pedido en la tabla `Pedido` con estado inicial `«pendiente»` y clave autoincremental `idPedido`.
   - Se descuenta la cantidad solicitada en la tabla `Inventario`.
   - Si el stock restante tras descontar las unidades es **mayor o igual a 10** (`nuevoStock >= 10`), se inserta el envío en la tabla `Envio` y el pedido pasa a estado `«enviado»`, confirmando la transacción con **`commit()`**.
   - Si el stock restante es **inferior a 10** (`nuevoStock < 10`), el pedido no puede completarse y se revierten todas las operaciones mediante **`rollback()`**.

---

## 🗄️ 2. Esquema de Base de Datos (PostgreSQL)

El proyecto incluye los scripts para reproducir la base de datos en pgAdmin:
* **`01_esquema_almacen.sql`**: Crea las tablas `Inventario`, `Pedido` y `Envio`.
* **`02_datos_almacen.sql`**: Inserta datos iniciales de inventario para pruebas.

---

## ⚙️ 3. Configuración

* **`config.properties`**: Archivo de configuración local con los datos de acceso a PostgreSQL:
  ```properties
  db.url=jdbc:postgresql://localhost:5432/almacen_pedidos
  db.user=postgres
  db.password=postgres
  ```
* **`config.example.properties`**: Plantilla de ejemplo sin contraseñas reales.

---

## 🧪 4. Casos de Prueba

Con los datos iniciales de `02_datos_almacen.sql`:
1. **Caso Exitoso (commit):**
   - Producto ID: `1` (Stock inicial: 50).
   - Cantidad pedida: `10`.
   - Stock resultante: `40` (>= 10).
   - **Resultado:** Pedido insertado, stock actualizado a 40, envío creado y pedido marcado como `«enviado»` (`commit`).
2. **Caso Rechazado por Stock Restante < 10 (rollback):**
   - Producto ID: `2` (Stock inicial: 15).
   - Cantidad pedida: `8`.
   - Stock resultante: `7` (< 10).
   - **Resultado:** Se cancela el pedido y se ejecuta `rollback()`. No se crea pedido ni envío, y el inventario permanece en 15.
3. **Caso Rechazado por Stock Insuficiente:**
   - Producto ID: `3` (Stock inicial: 5).
   - Cantidad pedida: `10`.
   - **Resultado:** No se inicia la transacción por falta de stock.
