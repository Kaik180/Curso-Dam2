# PLD Space: Gestión de Unidades y Ensayos de la Familia MIURA

**Módulo:** Acceso a Datos (2.º DAM)  
**Unidad:** UP 2 – Bases de Datos Relacionales – JDBC  
**Proyecto Maven:** `PLDSpaceLab`  

---

## 🚀 1. Descripción del Proyecto

Aplicación de consola en Java que gestiona las unidades de trabajo y las campañas de ensayos de lanzadores de la empresa aeroespacial **PLD Space** (lanzadores suborbitales **MIURA 1** y orbitales **MIURA 5**).

La arquitectura del proyecto sigue el patrón **POJO + DAO** con estricta separación de responsabilidades:
- **`model`**: Clases de entidad de la aplicación sin sentencias SQL (`Usuario`, `Unidad`).
- **`dao`**: Clases de acceso a datos (`UsuarioDAO`, `UnidadDAO`) con consultas parametrizadas mediante `PreparedStatement` para prevenir inyección SQL y control de filas afectadas.
- **`util`**: Centralización de la obtención de conexiones JDBC (`DatabaseConnection`) con configuración desacoplada y ciclo de vida controlado por `try-with-resources`.
- **`app`**: Punto de entrada con menú interactivo de consola (`MainApp`).

---

## 🗄️ 2. Preparación de la Base de Datos en PostgreSQL

1. Abre **pgAdmin** o tu terminal `psql` y crea la base de datos:
   ```sql
   CREATE DATABASE pldspace_lab;
   ```

2. Conéctate a la base de datos `pldspace_lab` y ejecuta secuencialmente los scripts incluidos en el proyecto:
   * **`01_esquema.sql`**: Crea las tablas `usuarios` y `unidades` junto con sus claves foráneas y restricciones `CHECK`:
     * `modelo`: sólo admite `'MIURA 1'` o `'MIURA 5'`.
     * `estado`: sólo admite `'PLANIFICADA'`, `'INTEGRACION'`, `'EN_ENSAYOS'` o `'REVISION'`.
   * **`02_datos.sql`**: Inserta usuarios técnicos y unidades iniciales (dejando unidades en estado diferente a `EN_ENSAYOS` para validar las transacciones).

---

## ⚙️ 3. Configuración de Credenciales

En la raíz del proyecto se incluye el archivo de plantilla:
* **`config.example.properties`** (sin claves reales, para entrega):
  ```properties
  db.url=jdbc:postgresql://localhost:5432/pldspace_lab
  db.user=postgres
  db.password=TU_CLAVE_LOCAL
  ```

Para ejecutar el proyecto en tu entorno local:
1. Crea una copia de `config.example.properties` llamada **`config.properties`** en la raíz del proyecto.
2. Introduce tu contraseña local de PostgreSQL en `db.password`.
> Nota: `config.properties` está excluido del control de versiones mediante `.gitignore` para cumplir con las directrices de seguridad.

---

## 💻 4. Ejecución del Programa

### Desde IntelliJ IDEA:
1. Abre la carpeta `PLDSpaceLab` como proyecto Maven en IntelliJ.
2. Navega a `src/main/java/app/MainApp.java`.
3. Haz clic derecho y selecciona **Run 'MainApp.main()'** (o `Shift + F10`).

### Credenciales de acceso de prueba:
| Usuario | Contraseña | Rol |
| :--- | :--- | :--- |
| `raul.torres` | `miura2023` | Ingeniero / Responsable |
| `pablo.gallego` | `tepida5` | Ingeniero / Responsable |
| `ingeniero.control` | `control123` | Control de Ensayos |

---

## 🧪 5. Pruebas y Validación Presencial

### A. Fase I: Autenticación
* **Acceso Permitido:** Introducir `raul.torres` y `miura2023`. El sistema dará la bienvenida y mostrará el menú.
* **Acceso Denegado:** Introducir un usuario o clave errónea. El sistema distingue entre fallo de credenciales y fallos técnicos de base de datos/configuración.

### B. Fase II: Menú CRUD
* **Opción 1 (Listar):** Muestra el código, modelo, estado y nombre del técnico responsable mediante un `JOIN`.
* **Opción 2 (Buscar):** Permite buscar por ID numérico o por código (ej. `M1-AULA01`).
* **Opción 3 (Insertar):** Inserta una nueva unidad validando modelo, estado y que el responsable exista.
* **Opción 4 (Modificar):** Actualiza el estado de una unidad.
* **Opción 5 (Eliminar):** Borra una unidad tras confirmación previa.

### C. Transacción Obligatoria: Campaña Conjunta de Ensayos (Opción 6)
El método `iniciarCampaniaPruebas(id1, id2)` ejecuta dos sentencias `UPDATE` sobre una **misma conexión** con `con.setAutoCommit(false)`:
1. **Prueba A (Transacción Exitosa con `commit()`):**
   * Seleccionar dos unidades existentes que no estén en `EN_ENSAYOS` (ej: IDs `1` y `2`).
   * Ambas pasarán atómicamente a `EN_ENSAYOS` y se confirmará la transacción.
2. **Prueba B (Transacción Fallida con `rollback()`):**
   * Seleccionar una unidad válida como primer ID (ej: `1`) y un ID inexistente como segundo ID (ej: `99999`).
   * Al afectar 0 filas el segundo UPDATE, el sistema lanza una excepción controlada y ejecuta `con.rollback()`.
   * **Comprobación:** La primera unidad mantiene su estado anterior sin guardar cambios parciales.
