package com.mutxamel.secops;

import java.io.IOException;
import java.sql.Connection;
import java.sql.SQLException;
import java.util.List;

public class MainApp {
    static LoginDAO loginDAO = new LoginDAO();
    static SoftwareAuditadoDAO softwareDAO = new SoftwareAuditadoDAO();

    public static void main(String[] args) {
        // 1. PRUEBA DE CONEXIÓN LEYENDO config.properties
        System.out.println("--- 1. Prueba de conexión externa (config.properties) ---");
        try (Connection con = DatabaseConnection.getConnection()) {
            System.out.println(" Conexión correcta con PostgreSQL desde config.properties.\n");
        } catch (IOException e) {
            System.out.println(" Error de configuración: " + e.getMessage());
            return;
        } catch (SQLException e) {
            System.out.println(" Error SQL: " + e.getMessage());
            return;
        }

        // 2. Operaciones de analistas (LoginDAO)
        System.out.println("=== PLANTILLA DE ANALISTAS (TABLA LOGIN) ===");
        if (loginDAO.buscarPorUserName("Silvia") == null) {
            Login silvia = new Login("Silvia", "silvia@silvia.es");
            loginDAO.insertarAnalista(silvia);
        }
        for (Login a : loginDAO.obtenerTodos()) {
            System.out.println(a);
        }

        // 3. Estado inicial de la tabla software_auditado
        System.out.println("\n=== ESTADO INICIAL DE SOFTWARE AUDITADO ===");
        List<SoftwareAuditado> inventarioInicial = softwareDAO.obtenerTodos();
        for (SoftwareAuditado app : inventarioInicial) {
            System.out.println(app);
        }

        // 4.Aseguramos que existan al menos dos registros para las pruebas transaccionales
        if (inventarioInicial.size() < 2) {
            softwareDAO.insertarSoftware(new SoftwareAuditado("Aplicación Base 1", 1));
            softwareDAO.insertarSoftware(new SoftwareAuditado("Aplicación Base 2", 1));
            inventarioInicial = softwareDAO.obtenerTodos();
        }

        int codigo1 = inventarioInicial.get(0).getCodigo();
        int codigo2 = inventarioInicial.get(1).getCodigo();

        // 5. COMPROBACIÓN DE TRANSACCIONES
        System.out.println("=== COMPROBACIÓN TRANSACCIONAL: commit() Y rollback() ======");

        // 6.1 PRUEBA A: Dos códigos existentes y distintos (commit) ---
        System.out.println("\n--- PRUEBA A: Transacción Exitosa (Códigos " + codigo1 + " y " + codigo2 + ") ---");
        System.out.println("Se actualizará código " + codigo1 + " a riesgo 4 y código " + codigo2 + " a riesgo 5.");
        boolean resultadoA = softwareDAO.actualizarDosNiveles(codigo1, 4, codigo2, 5);
        System.out.println("Resultado de la transacción A: " + (resultadoA ? "COMMIT CONFIRMADO (Éxito)" : "FALLO"));

        System.out.println("\nEstado tras Prueba A:");
        for (SoftwareAuditado app : softwareDAO.obtenerTodos()) {
            if (app.getCodigo() == codigo1 || app.getCodigo() == codigo2) {
                System.out.println(" -> " + app);
            }
        }

        // 6.2 PRUEBA B: El segundo código no existe (rollback) ---
        int codigoInexistente = 99999;
        System.out.println("\n--- PRUEBA B: Transacción Fallida Provocada (Códigos " + codigo1 + " y " + codigoInexistente + ") ---");
        System.out.println("Se intenta cambiar código " + codigo1 + " a riesgo 2 y código " + codigoInexistente + " a riesgo 3.");
        boolean resultadoB = softwareDAO.actualizarDosNiveles(codigo1, 2, codigoInexistente, 3);
        System.out.println("Resultado de la transacción B: " + (resultadoB ? "ÉXITO" : "ROLLBACK EJECUTADO (Operación revertida)"));

        System.out.println("\nEstado tras Prueba B (comprobación de atomicidad):");
        for (SoftwareAuditado app : softwareDAO.obtenerTodos()) {
            if (app.getCodigo() == codigo1) {
                System.out.println(" -> " + app);
                if (app.getNivelExposicion() != null && app.getNivelExposicion() == 4) {
                    System.out.println("    ✓ ¡Correcto! El código " + codigo1 + " conserva su valor 4 gracias a rollback().");
                }
            }
        }

        // Resumen final de todo el inventario
        System.out.println("\n=== INVENTARIO COMPLETO FINAL ===");
        for (SoftwareAuditado app : softwareDAO.obtenerTodos()) {
            System.out.println(app);
        }
    }
}
