package ud2.dao;

import ud2.model.SoftwareAuditado;
import ud2.util.DatabaseConnection;

import java.io.IOException;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class SoftwareAuditadoDAO {

    public List<SoftwareAuditado> obtenerTodos() {
        List<SoftwareAuditado> lista = new ArrayList<>();
        String sql = "SELECT codigo, nombre, nivel_exposicion FROM software_auditado ORDER BY codigo ASC";
        try (Connection con = DatabaseConnection.getConnection();
             Statement stmt = con.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                SoftwareAuditado app = new SoftwareAuditado(
                        rs.getInt("codigo"),
                        rs.getString("nombre"),
                        rs.getObject("nivel_exposicion", Integer.class)
                );
                lista.add(app);
            }
        } catch (IOException | SQLException e) {
            System.err.printf("Error al listar software (%s): %s%n",
                    (e instanceof SQLException) ? ((SQLException) e).getSQLState() : "IO", e.getMessage());
        }
        return lista;
    }

    public List<SoftwareAuditado> buscarPorRiesgoMinimo(int riesgoMinimo) {
        List<SoftwareAuditado> filtrada = new ArrayList<>();
        String sql = "SELECT codigo, nombre, nivel_exposicion FROM software_auditado WHERE nivel_exposicion >= ?";
        try (Connection con = DatabaseConnection.getConnection();
             PreparedStatement ps = con.prepareStatement(sql)) {
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
        } catch (IOException | SQLException e) {
            System.err.printf("Error al filtrar software (%s): %s%n",
                    (e instanceof SQLException) ? ((SQLException) e).getSQLState() : "IO", e.getMessage());
        }
        return filtrada;
    }

    public boolean insertarSoftware(SoftwareAuditado app) {
        String sql = "INSERT INTO software_auditado (nombre, nivel_exposicion) VALUES (?, ?)";
        try (Connection con = DatabaseConnection.getConnection();
             PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setString(1, app.getNombre());

            if (app.getNivelExposicion() == null) {
                ps.setObject(2, app.getNivelExposicion(), Types.INTEGER);
            } else {
                ps.setInt(2, app.getNivelExposicion());
            }

            int filasAfectadas = ps.executeUpdate();
            return filasAfectadas > 0;
        } catch (IOException | SQLException e) {
            System.err.printf("Error en insertar software (%s): %s%n",
                    (e instanceof SQLException) ? ((SQLException) e).getSQLState() : "IO", e.getMessage());
            return false;
        }
    }

    public boolean actualizarNivelRiesgo(int codigo, int nuevoNivel) {
        String sql = "UPDATE software_auditado SET nivel_exposicion = ? WHERE codigo = ?";
        try (Connection con = DatabaseConnection.getConnection();
             PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setInt(1, nuevoNivel);
            ps.setInt(2, codigo);

            int filasModificadas = ps.executeUpdate();
            return filasModificadas > 0;
        } catch (IOException | SQLException e) {
            System.err.printf("Error en actualizar nivel de riesgo (%s): %s%n",
                    (e instanceof SQLException) ? ((SQLException) e).getSQLState() : "IO", e.getMessage());
            return false;
        }
    }

    public boolean eliminarSoftware(int codigo) {
        String sql = "DELETE FROM software_auditado WHERE codigo = ?";
        try (Connection con = DatabaseConnection.getConnection();
             PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setInt(1, codigo);

            int filasEliminadas = ps.executeUpdate();
            return filasEliminadas > 0;
        } catch (IOException | SQLException e) {
            System.err.printf("Error en eliminar software (%s): %s%n",
                    (e instanceof SQLException) ? ((SQLException) e).getSQLState() : "IO", e.getMessage());
            return false;
        }
    }

    public List<SoftwareAuditado> buscarSoftwarePorNombre(String palabra) {
        List<SoftwareAuditado> filtrada = new ArrayList<>();
        String sql = "SELECT codigo, nombre, nivel_exposicion FROM software_auditado WHERE nombre ILIKE ?";
        try (Connection con = DatabaseConnection.getConnection();
             PreparedStatement ps = con.prepareStatement(sql)) {
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
        } catch (IOException | SQLException e) {
            System.err.printf("Error en buscar software por nombre (%s): %s%n",
                    (e instanceof SQLException) ? ((SQLException) e).getSQLState() : "IO", e.getMessage());
        }
        return filtrada;
    }

    public boolean actualizarDosNiveles(int codigo1, int nivel1, int codigo2, int nivel2) {
        String sql = "UPDATE software_auditado SET nivel_exposicion = ? WHERE codigo = ?";
        if (codigo1 == codigo2) {
            System.out.println("Debes indicar dos aplicaciones distintas.");
            return false;
        }

        try (Connection con = DatabaseConnection.getConnection()) {
            con.setAutoCommit(false);

            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setInt(1, nivel1);
                ps.setInt(2, codigo1);
                int filas1 = ps.executeUpdate();
                if (filas1 != 1) {
                    throw new SQLException("Primer registro inexistente.");
                }

                ps.setInt(1, nivel2);
                ps.setInt(2, codigo2);
                int filas2 = ps.executeUpdate();
                if (filas2 != 1) {
                    throw new SQLException("Segundo registro inexistente.");
                }

                con.commit();
                return true;
            } catch (SQLException e) {
                try {
                    con.rollback();
                } catch (SQLException errorRollback) {
                    System.out.println("Error al deshacer: " + errorRollback.getMessage());
                }
                System.out.println("Transacción cancelada: " + e.getMessage());
                return false;
            }
        } catch (IOException | SQLException e) {
            System.out.println("Error de conexión o configuración: " + e.getMessage());
            return false;
        }
    }

    public int insertarYObtenerCodigo(String nombre, int nivel) {
        String sql = "INSERT INTO software_auditado (nombre, nivel_exposicion) VALUES (?, ?)";
        try (Connection con = DatabaseConnection.getConnection();
             PreparedStatement ps = con.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setString(1, nombre);
            ps.setInt(2, nivel);

            if (ps.executeUpdate() != 1) {
                return -1;
            }

            try (ResultSet claves = ps.getGeneratedKeys()) {
                if (claves.next()) {
                    return claves.getInt(1);
                }
            }
        } catch (IOException | SQLException e) {
            System.out.println("No se pudo insertar: " + e.getMessage());
        }
        return -1;
    }

    public boolean registrarSoftwareConIncidencia(String nombre, int nivel, String descripcion) {
        String sqlSoftware = "INSERT INTO software_auditado (nombre, nivel_exposicion) VALUES (?, ?)";
        String sqlIncidencia = "INSERT INTO incidencias (software_codigo, descripcion) VALUES (?, ?)";

        try (Connection con = DatabaseConnection.getConnection()) {
            con.setAutoCommit(false);
            try {
                int codigo;
                try (PreparedStatement ps = con.prepareStatement(sqlSoftware, Statement.RETURN_GENERATED_KEYS)) {
                    ps.setString(1, nombre);
                    ps.setInt(2, nivel);

                    if (ps.executeUpdate() != 1) {
                        throw new SQLException("No se insertó el software.");
                    }

                    try (ResultSet claves = ps.getGeneratedKeys()) {
                        if (!claves.next()) {
                            throw new SQLException("No se obtuvo la clave.");
                        }
                        codigo = claves.getInt(1);
                    }
                }

                try (PreparedStatement ps = con.prepareStatement(sqlIncidencia)) {
                    ps.setInt(1, codigo);
                    ps.setString(2, descripcion);

                    if (ps.executeUpdate() != 1) {
                        throw new SQLException("No se insertó la incidencia.");
                    }
                }

                con.commit();
                return true;

            } catch (SQLException e) {
                try {
                    con.rollback();
                } catch (SQLException errorRollback) {
                    System.err.println("Error al deshacer: " + errorRollback.getMessage());
                }
                System.err.println("Registro cancelado: " + e.getMessage());
                return false;
            }
        } catch (IOException | SQLException e) {
            System.err.println("Error de conexión: " + e.getMessage());
            return false;
        }
    }
}
