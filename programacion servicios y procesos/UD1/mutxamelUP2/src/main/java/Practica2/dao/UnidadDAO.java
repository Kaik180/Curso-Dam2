package Practica2.dao;

import Practica2.model.Unidad;
import Practica2.util.DatabaseConnection;

import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class UnidadDAO {


    public List<Unidad> obtenerTodas() throws IOException, SQLException {
        List<Unidad> lista = new ArrayList<>();
        String sql = "SELECT u.id, u.codigo, u.modelo, u.estado, u.responsable_id, us.usuario AS resp_nombre " +
                     "FROM unidades u " +
                     "JOIN usuarios us ON u.responsable_id = us.id " +
                     "ORDER BY u.id ASC";

        try (Connection con = DatabaseConnection.getConnection();
             PreparedStatement ps = con.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {

            while (rs.next()) {
                lista.add(new Unidad(
                        rs.getInt("id"),
                        rs.getString("codigo"),
                        rs.getString("modelo"),
                        rs.getString("estado"),
                        rs.getInt("responsable_id"),
                        rs.getString("resp_nombre")
                ));
            }
        }
        return lista;
    }


     // 2. Buscar una unidad por su identificador numérico (id).

    public Unidad buscarPorId(int id) throws IOException, SQLException {
        String sql = "SELECT u.id, u.codigo, u.modelo, u.estado, u.responsable_id, us.usuario AS resp_nombre " +
                     "FROM unidades u " +
                     "JOIN usuarios us ON u.responsable_id = us.id " +
                     "WHERE u.id = ?";

        try (Connection con = DatabaseConnection.getConnection();
             PreparedStatement ps = con.prepareStatement(sql)) {

            ps.setInt(1, id);
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    return new Unidad(
                            rs.getInt("id"),
                            rs.getString("codigo"),
                            rs.getString("modelo"),
                            rs.getString("estado"),
                            rs.getInt("responsable_id"),
                            rs.getString("resp_nombre")
                    );
                }
            }
        }
        return null;
    }


     //Búsqueda complementaria por código alfanumérico (ej: M1-AULA01).

    public Unidad buscarPorCodigo(String codigo) throws IOException, SQLException {
        String sql = "SELECT u.id, u.codigo, u.modelo, u.estado, u.responsable_id, us.usuario AS resp_nombre " +
                     "FROM unidades u " +
                     "JOIN usuarios us ON u.responsable_id = us.id " +
                     "WHERE u.codigo = ?";

        try (Connection con = DatabaseConnection.getConnection();
             PreparedStatement ps = con.prepareStatement(sql)) {

            ps.setString(1, codigo);
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    return new Unidad(
                            rs.getInt("id"),
                            rs.getString("codigo"),
                            rs.getString("modelo"),
                            rs.getString("estado"),
                            rs.getInt("responsable_id"),
                            rs.getString("resp_nombre")
                    );
                }
            }
        }
        return null;
    }

    // 3. Insertar una nueva unidad, asignándola a un responsable existente.

    public boolean insertar(Unidad unidad) throws IOException, SQLException {
        String sql = "INSERT INTO unidades (codigo, modelo, estado, responsable_id) VALUES (?, ?, ?, ?)";

        try (Connection con = DatabaseConnection.getConnection();
             PreparedStatement ps = con.prepareStatement(sql)) {

            ps.setString(1, unidad.getCodigo());
            ps.setString(2, unidad.getModelo());
            ps.setString(3, unidad.getEstado());
            ps.setInt(4, unidad.getResponsableId());

            int filas = ps.executeUpdate();
            return filas > 0;
        }
    }


     // 4. Modificar el estado de una unidad existente.

    public boolean modificarEstado(int id, String nuevoEstado) throws IOException, SQLException {
        String sql = "UPDATE unidades SET estado = ? WHERE id = ?";

        try (Connection con = DatabaseConnection.getConnection();
             PreparedStatement ps = con.prepareStatement(sql)) {

            ps.setString(1, nuevoEstado);
            ps.setInt(2, id);

            int filas = ps.executeUpdate();
            return filas > 0;
        }
    }

    // 5. Eliminar una unidad por su identificador.

    public boolean eliminarPorId(int id) throws IOException, SQLException {
        String sql = "DELETE FROM unidades WHERE id = ?";

        try (Connection con = DatabaseConnection.getConnection();
             PreparedStatement ps = con.prepareStatement(sql)) {

            ps.setInt(1, id);
            int filas = ps.executeUpdate();
            return filas > 0;
        }
    }

    // 6. Transacción obligatoria: campaña conjunta de pruebas
    public boolean iniciarCampaniaPruebas(int id1, int id2) throws IOException, SQLException {
        if (id1 == id2) {
            System.err.println("✗ Error: Debe indicar dos identificadores de unidades distintos.");
            return false;
        }

        String sql = "UPDATE unidades SET estado = 'EN_ENSAYOS' WHERE id = ?";

        try (Connection con = DatabaseConnection.getConnection()) {
            con.setAutoCommit(false); // Inicia de la transacción

            try (PreparedStatement ps = con.prepareStatement(sql)) {
                // 6.1. Actualizar primera unidad
                ps.setInt(1, id1);
                int filas1 = ps.executeUpdate();
                if (filas1 != 1) {
                    throw new SQLException("La primera unidad con ID " + id1 + " no existe (filas afectadas: " + filas1 + ").");
                }

                // 6.2. Actualizar segunda unidad
                ps.setInt(1, id2);
                int filas2 = ps.executeUpdate();
                if (filas2 != 1) {
                    throw new SQLException("La segunda unidad con ID " + id2 + " no existe (filas afectadas: " + filas2 + ").");
                }

                // 6.3. Confirmar la transacción completa
                con.commit();
                System.out.println("✓ Transacción confirmada (commit): Las unidades " + id1 + " y " + id2 + " han pasado a 'EN_ENSAYOS'.");
                return true;

            } catch (SQLException e) {
                // 6.4. Revertir cambios en caso de fallo (filas != 1)
                try {
                    con.rollback();
                    System.err.println("⚠ Se ha ejecutado rollback() para mantener la atomicidad.");
                } catch (SQLException rbEx) {
                    System.err.println("Error grave durante rollback: " + rbEx.getMessage());
                }
                System.err.println("✗ Transacción cancelada: " + e.getMessage());
                return false;
            }
        }
    }
}
