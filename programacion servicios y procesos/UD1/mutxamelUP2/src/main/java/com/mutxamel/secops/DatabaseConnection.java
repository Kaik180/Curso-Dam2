package com.mutxamel.secops;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DatabaseConnection {
    private static Connection connection = null;
    private DatabaseConnection() {}
    static {
        //las claves de acceso para poder conectarse, las 3 cosas de abajo son la clave para conecction
        String url = "jdbc:postgresql://localhost:5432/mutxamel_pg";
        String user = "postgres";
        String password = "postgres";
        try {
            connection = DriverManager.getConnection(url, user, password);
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
    public static Connection getConnection() {
        return connection;
    }
}

