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

    /**
     * Obtiene una nueva conexión a PostgreSQL leyendo la configuración externa desde config.properties.
     * Cada llamada devuelve una conexión independiente para gestionar su ciclo de vida con try-with-resources.
     *
     * @return Connection activa con PostgreSQL
     * @throws SQLException si ocurre un error en la conexión o autenticación de la base de datos
     * @throws IOException  si no se encuentra o no se puede leer el archivo config.properties
     */
    public static Connection getConnection() throws SQLException, IOException {
        Properties propiedades = new Properties();

        // Intenta abrir config.properties en la raíz del proyecto
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
