package com.mutxamel.secops;

import com.mutxamel.secops.SoftwareAuditado;
import com.mutxamel.secops.DatabaseConnection;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;
public class SoftwareAuditadoDAO {
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
                            rs.getObject("nivel_exposicion", Integer.class) // Lectura segura deposibles NULL
                    );
                    lista.add(app);
                }
            }
        } catch (SQLException e) {
            System.err.printf("Error SQL al listar software (%s): %s%n", e.getSQLState(),
                    e.getMessage());
        }
        return lista;
    }
    // 2. READ (Filtrado): Buscar aplicaciones cuyo riesgo sea mayor o igual al mínimoindicado
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
            System.err.printf("Error SQL al filtrar software (%s): %s%n", e.getSQLState(),
                    e.getMessage());
        }
        return filtrada;
    }
}

