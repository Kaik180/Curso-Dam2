package com.mutxamel.secops.Proyecto.dao;

import com.mutxamel.secops.Proyecto.model.Envio;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class EnvioDao {

    public boolean insertarEnvio(Connection conn, Envio envio) throws SQLException {
        String sql = "INSERT INTO Envio (fechaEnvio, idProducto) VALUES (?, ?)";

        try (PreparedStatement ps = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setDate(1, envio.getFechaEnvio());
            ps.setInt(2, envio.getIdProducto());

            int filas = ps.executeUpdate();
            if (filas == 1) {
                try (ResultSet rs = ps.getGeneratedKeys()) {
                    if (rs.next()) {
                        envio.setIdEnvio(rs.getInt(1));
                    }
                }
                return true;
            }
            return false;
        }
    }
}
