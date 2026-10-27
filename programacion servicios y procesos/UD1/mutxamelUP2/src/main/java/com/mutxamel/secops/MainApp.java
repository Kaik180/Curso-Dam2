package com.mutxamel.secops;

import com.mutxamel.secops.DatabaseConnection;
import com.mutxamel.secops.LoginDAO;
import com.mutxamel.secops.SoftwareAuditadoDAO;
import com.mutxamel.secops.Login;
import com.mutxamel.secops.SoftwareAuditado;
import java.sql.Connection;
import java.sql.SQLException;
import java.util.List;

public class MainApp {
    static LoginDAO loginDAO = new LoginDAO();
    static SoftwareAuditadoDAO softwareDAO = new SoftwareAuditadoDAO();
    public static void main(String[] args) {


        //Consigue el databaseconnection = las claves de acceso para conectarse a la base de datos y intnta conectarse
        try (Connection con = DatabaseConnection.getConnection()) {
            if (con != null && !con.isClosed()) {
                System.out.println("BD conectada correctamente.");
            } else {
                throw new SQLException();
            }
        } catch (SQLException e) {
            muestraErrorSQL(e);
        }
    }

    public static void muestraErrorSQL(SQLException e) {
        System.err.printf("Ups, hemos detectado un problema con la DB! %n");
        System.err.printf("¿Qué ha pasado?: %s%n", e.getMessage());
        System.err.printf("Código de estado (SQLState): %s%n", e.getSQLState());
        System.err.printf("Código interno del motor: %d%n", e.getErrorCode());
        SQLException next = e.getNextException();
        while (next != null) {
            System.err.printf(" -> Además,provocó este otro fallo: %s (Estado: %s)%n",
                    next.getMessage(), next.getSQLState());
            next = next.getNextException();
        }
        // 1. Insertamos o verificamos a la analista Silvia en PostgreSQL
        if (loginDAO.buscarPorUserName("Silvia") == null) {
            Login silvia = new Login("Silvia", "silvia@silvia.es");
            if (loginDAO.insertarAnalista(silvia)) {
                System.out.println("Analista Silvia registrada con éxito en mutxamel_pg.");
            }
        }
        // 2. Listamos todos los analistas persistidos en la tabla 'login'
        System.out.println("\n=== PLANTILLA DE ANALISTAS (TABLA LOGIN) ===");
        List<Login> analistas = loginDAO.obtenerTodos();
        for (Login a : analistas) {
            System.out.println(a);
        }
        // 3. Listamos el inventario completo de software auditado
        System.out.println("\n=== INVENTARIO DE SOFTWARE AUDITADO ===");
        List<SoftwareAuditado> inventario = softwareDAO.obtenerTodos();
        for (SoftwareAuditado app : inventario) {
            System.out.println(app);
        }
        // 4. Consultamos aplicaciones críticas (nivel de exposición >= 4)
        System.out.println("\n=== ALERTA SEC-OPS: SOFTWARE CRÍTICO (RIESGO >= 4) ===");
        List<SoftwareAuditado> criticas = softwareDAO.buscarPorRiesgoMinimo(4);
        for (SoftwareAuditado app : criticas) {
            System.out.println(app);
        }
    }
}