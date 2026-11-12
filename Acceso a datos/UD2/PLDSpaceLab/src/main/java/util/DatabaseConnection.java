package util;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Properties;

public class DatabaseConnection {

    private DatabaseConnection() {
    }

    public static Connection getConnection() throws SQLException, IOException {
        Properties propiedades = new Properties();

        Path rutaConfig = Path.of("config.properties");
        try (InputStream entrada = Files.newInputStream(rutaConfig)) {
            propiedades.load(entrada);
        }

        String url = propiedades.getProperty("db.url");
        String usuario = propiedades.getProperty("db.user");
        String password = propiedades.getProperty("db.password");

        if (url == null || usuario == null || password == null) {
            throw new IOException("Faltan propiedades de conexión obligatorias en config.properties (db.url, db.user, db.password).");
        }

        return DriverManager.getConnection(url, usuario, password);
    }
}
