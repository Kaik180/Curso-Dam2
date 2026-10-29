package com.mutxamel.secops;

import com.mutxamel.secops.SoftwareAuditado;
import com.mutxamel.secops.DatabaseConnection;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class SoftwareAuditadoDAO2 {

    // 1. READ: Listar todo el inventario de software auditado
    public List<SoftwareAuditado> obtenerTodos() {
        List<SoftwareAuditado> lista = new ArrayList<>();
        String sql = "SELECT codigo, nombre, nivel_exposicion FROM software_auditado ORDER BY codigo ASC";
        try {
            Connection con = DatabaseConnection.getConnection();
            try (Statement stmt = con.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                while (rs.next()) {
                    SoftwareAuditado app = new SoftwareAuditado(
                            rs.getInt("codigo"),
                            rs.getString("nombre"),
                            rs.getObject("nivel_exposicion", Integer.class)
                    );
                    lista.add(app);
                }
            }
        } catch (SQLException e) {
            System.err.printf("Error SQL al listar software (%s): %s%n", e.getSQLState(), e.getMessage());
        }
        return lista;
    }

    // 2. READ (Filtrado): Buscar aplicaciones cuyo riesgo sea mayor o igual al mínimo indicado
    public List<SoftwareAuditado> buscarPorRiesgoMinimo(int riesgoMinimo) {
        List<SoftwareAuditado> filtrada = new ArrayList<>();
        String sql = "SELECT codigo, nombre, nivel_exposicion FROM software_auditado WHERE nivel_exposicion >= ?";
        try {
            Connection con = DatabaseConnection.getConnection();
            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setInt(1, riesgoMinimo);
                try (ResultSet rs = ps.executeQuery()) {
                    while (rs.next()) {
                        SoftwareAuditado app = new SoftwareAuditado(
                                rs.getInt("codigo"),
                                rs.getString("nombre"),
                                rs.getObject("nivel_exposicion", Integer.class)
                        );
                        filtrada.add(app);
                    }
                }
            }
        } catch (SQLException e) {
            System.err.printf("Error SQL al filtrar software (%s): %s%n", e.getSQLState(), e.getMessage());
        }
        return filtrada;
    }

    // 1. Inserción con control de nulos
    public boolean insertarSoftware(SoftwareAuditado app) {
        String sql = "INSERT INTO software_auditado (nombre, nivel_exposicion) VALUES (?, ?)";
        try {
            Connection con = DatabaseConnection.getConnection();
            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setString(1, app.getNombre());

                if (app.getNivelExposicion() == null) {
                    ps.setObject(2, app.getNivelExposicion(), Types.INTEGER);
                } else {
                    ps.setInt(2, app.getNivelExposicion());
                }

                int filasAfectadas = ps.executeUpdate();
                return filasAfectadas > 0;
            }
        } catch (SQLException e) {
            System.err.printf("Error SQL en insertar software (%s): %s%n", e.getSQLState(), e.getMessage());
            return false;
        }
    }

    // 2. Actualización
    public boolean actualizarNivelRiesgo(int codigo, int nuevoNivel) {
        String sql = "UPDATE software_auditado SET nivel_exposicion = ? WHERE codigo = ?";
        try {
            Connection con = DatabaseConnection.getConnection();
            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setInt(1, nuevoNivel);
                ps.setInt(2, codigo);

                int filasModificadas = ps.executeUpdate();
                return filasModificadas > 0;
            }
        } catch (SQLException e) {
            System.err.printf("Error SQL en actualizar nivel de riesgo (%s): %s%n", e.getSQLState(), e.getMessage());
            return false;
        }
    }

    // 3. Borrado
    public boolean eliminarSoftware(int codigo) {
        String sql = "DELETE FROM software_auditado WHERE codigo = ?";
        try {
            Connection con = DatabaseConnection.getConnection();
            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setInt(1, codigo);

                int filasEliminadas = ps.executeUpdate();
                return filasEliminadas > 0;
            }
        } catch (SQLException e) {
            System.err.printf("Error SQL en eliminar software (%s): %s%n", e.getSQLState(), e.getMessage());
            return false;
        }
    }

    // 4. Búsqueda por aproximación
    public List<SoftwareAuditado> buscarSoftwarePorNombre(String palabra) {
        List<SoftwareAuditado> filtrada = new ArrayList<>();
        String sql = "SELECT codigo, nombre, nivel_exposicion FROM software_auditado WHERE nombre ILIKE ?";
        try {
            Connection con = DatabaseConnection.getConnection();
            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setString(1, "%" + palabra + "%");

                try (ResultSet rs = ps.executeQuery()) {
                    while (rs.next()) {
                        SoftwareAuditado app = new SoftwareAuditado(
                                rs.getInt("codigo"),
                                rs.getString("nombre"),
                                rs.getObject("nivel_exposicion", Integer.class)
                        );
                        filtrada.add(app);
                    }
                }
            }
        } catch (SQLException e) {
            System.err.printf("Error SQL en buscar software por nombre (%s): %s%n", e.getSQLState(), e.getMessage());
        }
        return filtrada;
    }
}
