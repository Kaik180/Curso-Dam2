package com.mutxamel.secops;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class JDBCConnectionDiagnostic {
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
    }

    public static void main(String[] args) {
        String urlPg = "jdbc:postgresql://localhost:5432/mutxamel_pg";

        // try-with-resources cierra la conexión automáticamente al implementar AutoCloseable
        try (Connection con = DriverManager.getConnection(urlPg, "postgres", "postgress")) {
            System.out.println("¡Genial! Hemos conectado a la base de datos con éxito.");
            System.out.printf("Estamos trabajando con: %s%n",
                    con.getMetaData().getDatabaseProductName());
        } catch (SQLException ex) {
            muestraErrorSQL(ex);
        }

    }
}