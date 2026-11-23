package com.mutxamel.secops.Proyecto.util;

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
        Path ruta = Path.of("config.properties");

        if (!Files.exists(ruta)) {
            // Intento alternativo en caso de ejecutarse desde una subcarpeta o raíz distinta
            Path rutaAlt = Path.of("Acceso a datos/UD2/UP2_AlmacenPedidos/config.properties");
            if (Files.exists(rutaAlt)) {
                ruta = rutaAlt;
            }
        }

        if (Files.exists(ruta)) {
            try (InputStream entrada = Files.newInputStream(ruta)) {
                propiedades.load(entrada);
            }
        }

        String url = propiedades.getProperty("db.url", "jdbc:postgresql://localhost:5432/almacen_pedidos");
        String usuario = propiedades.getProperty("db.user", "postgres");
        String password = propiedades.getProperty("db.password", "postgres");

        return DriverManager.getConnection(url, usuario, password);
    }
}
