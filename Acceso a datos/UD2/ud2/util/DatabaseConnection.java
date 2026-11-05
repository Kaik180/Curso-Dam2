package com.mutxamel.secops.Practica1.ud2.util;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Properties;

public class DatabaseConnection {

    private DatabaseConnection() { }

    public static Connection getConnection() throws SQLException, IOException {
        Properties propiedades = new Properties();
        try (InputStream entrada = Files.newInputStream(Path.of("config.properties"))) {
            propiedades.load(entrada);
        }

        String url = propiedades.getProperty("db.url");
        String usuario = propiedades.getProperty("db.user");
        String password = propiedades.getProperty("db.password");

        if (url == null || usuario == null || password == null) {
            throw new IOException("Faltan propiedades de conexión.");
        }

        return DriverManager.getConnection(url, usuario, password);
    }
}
