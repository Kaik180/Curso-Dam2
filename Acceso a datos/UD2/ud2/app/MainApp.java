package ud2.app;

import ud2.dao.LoginDAO;
import ud2.dao.SoftwareAuditadoDAO;
import ud2.model.Login;
import ud2.model.SoftwareAuditado;
import ud2.util.DatabaseConnection;

import java.io.IOException;
import java.sql.Connection;
import java.sql.SQLException;
import java.util.List;

public class MainApp {
    static LoginDAO loginDAO = new LoginDAO();
    static SoftwareAuditadoDAO softwareDAO = new SoftwareAuditadoDAO();

    public static void main(String[] args) {
        System.out.println("=============================================================");
        System.out.println("  MUTXAMEL SEC-OPS S.L. - GESTIÓN Y PERSISTENCIA JDBC");
        System.out.println("=============================================================\n");

        System.out.println("--- 1. Prueba de conexión externa (config.properties) ---");
        try (Connection con = DatabaseConnection.getConnection()) {
            System.out.println("✓ Conexión correcta con PostgreSQL desde config.properties.\n");
        } catch (IOException e) {
            System.out.println("✗ Error de configuración: " + e.getMessage());
            return;
        } catch (SQLException e) {
            System.out.println("✗ Error SQL: " + e.getMessage());
            return;
        }

        System.out.println("=== PLANTILLA DE ANALISTAS (TABLA LOGIN) ===");
        if (loginDAO.buscarPorUserName("Silvia") == null) {
            Login silvia = new Login("Silvia", "silvia@silvia.es");
            loginDAO.insertarAnalista(silvia);
        }
        for (Login a : loginDAO.obtenerTodos()) {
            System.out.println(a);
        }

        System.out.println("\n=== ESTADO INICIAL DE SOFTWARE AUDITADO ===");
        List<SoftwareAuditado> inventarioInicial = softwareDAO.obtenerTodos();
        for (SoftwareAuditado app : inventarioInicial) {
            System.out.println(app);
        }

        if (inventarioInicial.size() < 2) {
            softwareDAO.insertarSoftware(new SoftwareAuditado("Aplicación Base 1", 1));
            softwareDAO.insertarSoftware(new SoftwareAuditado("Aplicación Base 2", 1));
            inventarioInicial = softwareDAO.obtenerTodos();
        }

        int codigo1 = inventarioInicial.get(0).getCodigo();
        int codigo2 = inventarioInicial.get(1).getCodigo();

        System.out.println("\n=== COMPROBACIÓN TRANSACCIONAL: commit() Y rollback() (Sesión 4) ===");
        System.out.println("\n--- PRUEBA A: Transacción Exitosa (Códigos " + codigo1 + " y " + codigo2 + ") ---");
        boolean resultadoA = softwareDAO.actualizarDosNiveles(codigo1, 4, codigo2, 5);
        System.out.println("Resultado de la transacción A: " + (resultadoA ? "COMMIT CONFIRMADO (Éxito)" : "FALLO"));

        int codigoInexistente = 99999;
        System.out.println("\n--- PRUEBA B: Transacción Fallida Provocada (Códigos " + codigo1 + " y " + codigoInexistente + ") ---");
        boolean resultadoB = softwareDAO.actualizarDosNiveles(codigo1, 2, codigoInexistente, 3);
        System.out.println("Resultado de la transacción B: " + (resultadoB ? "ÉXITO" : "ROLLBACK EJECUTADO (Operación revertida)"));

        System.out.println("\n=============================================================");
        System.out.println("=== SESIÓN 5: RETO DE CLAVES AUTOGENERADAS Y TRANSACCIÓN ===");
        System.out.println("=============================================================");

        System.out.println("\n--- 1. Inserción y recuperación de clave generada ---");
        String nombreAppAutogenerada = "Firewall WAF Cloud";
        int claveGenerada = softwareDAO.insertarYObtenerCodigo(nombreAppAutogenerada, 3);
        if (claveGenerada != -1) {
            System.out.println("✓ Aplicación '" + nombreAppAutogenerada + "' insertada con éxito.");
            System.out.println("✓ Clave autogenerada recuperada por PostgreSQL (codigo): " + claveGenerada);
        } else {
            System.out.println("✗ Error al insertar la aplicación y obtener la clave.");
        }

        System.out.println("\n--- 2. Transacción de registros relacionados (Software + Incidencia) ---");
        String nombreAppConIncidencia = "Servidor Proxy NGINX";
        String descripcionIncidencia = "Vulnerabilidad de desbordamiento de búfer detectada en puerto 443.";
        boolean regExitoso = softwareDAO.registrarSoftwareConIncidencia(nombreAppConIncidencia, 4, descripcionIncidencia);
        System.out.println("Resultado del registro conjunto: " + (regExitoso ? "COMMIT EXITOSO (Ambos registros guardados y relacionados)" : "FALLÓ"));

        System.out.println("\n--- 3. Fallo intencionado en incidencia (descripción NULL) -> rollback() ---");
        String nombreAppFallida = "Herramienta Backup Incompleta";
        System.out.println("Intentando insertar '" + nombreAppFallida + "' con incidencia NULL...");
        boolean regFallido = softwareDAO.registrarSoftwareConIncidencia(nombreAppFallida, 1, null);
        System.out.println("Resultado del intento: " + (regFallido ? "INCORRECTO (no debería confirmarse)" : "ROLLBACK EJECUTADO (Ningún cambio guardado)"));

        List<SoftwareAuditado> busquedaAppFallida = softwareDAO.buscarSoftwarePorNombre("Backup Incompleta");
        if (busquedaAppFallida.isEmpty()) {
            System.out.println("✓ ¡Verificación correcta! '" + nombreAppFallida + "' no existe en la BD gracias a rollback().");
        } else {
            System.out.println("✗ Error: La aplicación quedó guardada en la base de datos sin su incidencia.");
        }

        System.out.println("\n=== INVENTARIO FINAL DE SOFTWARE TRAS SESIÓN 5 ===");
        for (SoftwareAuditado app : softwareDAO.obtenerTodos()) {
            System.out.println(app);
        }
    }
}
