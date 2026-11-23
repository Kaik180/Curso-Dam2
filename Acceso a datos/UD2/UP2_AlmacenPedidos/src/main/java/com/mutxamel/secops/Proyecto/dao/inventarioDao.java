package com.mutxamel.secops.Proyecto.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class inventarioDao {

    public int consultarStock(Connection conn, int idProducto) throws SQLException {
        String sql = "SELECT stock FROM Inventario WHERE idProducto = ?";

        try (PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setInt(1, idProducto);

            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt("stock");
                }
            }
        }
        return -1; // El producto no existe en la tabla Inventario
    }

    public boolean actualizarStock(Connection conn, int idProducto, int nuevoStock) throws SQLException {
        String sql = "UPDATE Inventario SET stock = ? WHERE idProducto = ?";

        try (PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setInt(1, nuevoStock);
            ps.setInt(2, idProducto);

            int filas = ps.executeUpdate();
            return filas == 1;
        }
    }
}
