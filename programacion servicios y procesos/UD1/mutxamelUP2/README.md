# Proyecto Mutxamel Sec-Ops S.L. - mutxamelUP2

**Módulo:** Acceso a Datos (2.º DAM)  
**Unidad:** UP 2 – Bases de Datos Relacionales – JDBC  
**Sesión 5:** Claves Autogeneradas, Tablas Relacionadas y Rutinas SQL  

---

## 🚀 Contenido del Proyecto

1. **Configuración externa:** `config.example.properties` (sin credenciales reales) para configurar la conexión a `mutxamel_pg`.
2. **Scripts SQL:**
   - `00_esquema_mutxamel_pg.sql`: Esquema completo de las tablas `login`, `software_auditado` e `incidencias`.
   - `03_incidencias.sql`: Creación de la tabla relacionada `incidencias` con clave foránea a `software_auditado(codigo)`.
3. **Capa de Modelo (POJOs):** `Login`, `SoftwareAuditado`, `Incidencia`.
4. **Capa DAO:** `LoginDAO`, `SoftwareAuditadoDAO` con consultas parametrizadas, gestión de claves autogeneradas con `Statement.RETURN_GENERATED_KEYS` y `getGeneratedKeys()`, y transacciones atómicas (`commit`/`rollback`).
5. **Capa App:** `MainApp` con la batería de pruebas y demostración del reto.
