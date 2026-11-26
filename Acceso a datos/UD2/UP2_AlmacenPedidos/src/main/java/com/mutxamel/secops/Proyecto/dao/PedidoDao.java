package com.mutxamel.secops.Proyecto.dao;

import com.mutxamel.secops.Proyecto.model.Envio;
import com.mutxamel.secops.Proyecto.model.Pedido;
import com.mutxamel.secops.Proyecto.util.DatabaseConnection;

import java.io.IOException;
import java.sql.Connection;
import java.sql.Date;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

public class PedidoDao {

    private final inventarioDao inventarioDAO = new inventarioDao();
    private final EnvioDao envioDAO = new EnvioDao();

    public int insertarPedido(Connection conn, Pedido pedido) throws SQLException {
        String sql = "INSERT INTO Pedido (idCliente, fecha, status, idProducto, cantidad) VALUES (?, ?, ?, ?, ?)";

        try (PreparedStatement ps = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setInt(1, pedido.getIdCliente());
            ps.setDate(2, pedido.getFecha());
            ps.setString(3, pedido.getStatus());
            ps.setInt(4, pedido.getIdProducto());
            ps.setInt(5, pedido.getCantidad());

            int filas = ps.executeUpdate();
            if (filas == 1) {
                try (ResultSet rs = ps.getGeneratedKeys()) {
                    if (rs.next()) {
                        int idGenerado = rs.getInt(1);
                        pedido.setIdPedido(idGenerado);
                        return idGenerado;
                    }
                }
            }
        }
        return -1;
    }

    public boolean actualizarStatus(Connection conn, int idPedido, String nuevoStatus) throws SQLException {
        String sql = "UPDATE Pedido SET status = ? WHERE idPedido = ?";

        try (PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, nuevoStatus);
            ps.setInt(2, idPedido);

            int filas = ps.executeUpdate();
            return filas == 1;
        }
    }

    public void procesarPedido(Pedido pedido, int stockActualProducto) {
        try (Connection conn = DatabaseConnection.getConnection()) {
            conn.setAutoCommit(false);

            try {
                // 3. Insertar en la tabla Pedido el objeto pedido que se pasa por parámetro
                int idPedido = insertarPedido(conn, pedido);
                if (idPedido <= 0) {
                    throw new SQLException("No se pudo insertar el pedido en la base de datos.");
                }

                // 4. Calcular el nuevo stock del producto y actualizarlo en la tabla Inventario
                int nuevoStock = stockActualProducto - pedido.getCantidad();
                boolean stockActualizado = inventarioDAO.actualizarStock(conn, pedido.getIdProducto(), nuevoStock);
                if (!stockActualizado) {
                    throw new SQLException("Error al actualizar el stock del producto en la tabla Inventario.");
                }

                // 5. Insertar un nuevo envío únicamente si el stock resultante es >= 10
                if (nuevoStock < 10) {
                    throw new SQLException("El stock resultante (" + nuevoStock + " unidades) es inferior a 10. No se puede completar el pedido.");
                }

                Envio nuevoEnvio = new Envio(new Date(System.currentTimeMillis()), pedido.getIdProducto());
                boolean envioInsertado = envioDAO.insertarEnvio(conn, nuevoEnvio);
                if (!envioInsertado) {
                    throw new SQLException("Error al registrar el envío en la tabla Envio.");
                }

                // 6. Actualizar el campo status de la tabla Pedido, pasando a ser 'enviado'
                boolean statusActualizado = actualizarStatus(conn, idPedido, "enviado");
                if (!statusActualizado) {
                    throw new SQLException("Error al actualizar el estado del pedido a 'enviado'.");
                }
                pedido.setStatus("enviado");

                // Confirmar todas las modificaciones juntas si todo ha salido bien
                conn.commit();
                System.out.println("\n✓ [TRANSACCIÓN COMPLETADA]");
                System.out.println("  Pedido ID: " + idPedido + " registrado y ENVIADO.");
                System.out.println("  Stock restante actualizado a: " + nuevoStock + " unidades.");
                System.out.println("  Envío generado correctamente.");

            } catch (SQLException e) {
                // 7. Si falla la creación o actualización de cualquiera de los registros, rollback()
                try {
                    conn.rollback();
                    System.err.println("\n⚠ [TRANSACCIÓN CANCELADA - ROLLBACK]");
                    System.err.println("  Se han revertido todas las operaciones para mantener la consistencia de la base de datos.");
                } catch (SQLException rollbackEx) {
                    System.err.println("Error grave durante el rollback: " + rollbackEx.getMessage());
                }
                System.err.println("  Motivo: " + e.getMessage());
            }

        } catch (IOException e) {
            System.err.println("Error de configuración al abrir la conexión: " + e.getMessage());
        } catch (SQLException e) {
            System.err.println("Error de conexión a la base de datos: " + e.getMessage());
        }
    }

    public List<Pedido> obtenerTodos() throws IOException, SQLException {
        List<Pedido> lista = new ArrayList<>();
        String sql = "SELECT idPedido, idCliente, fecha, status, idProducto, cantidad FROM Pedido ORDER BY idPedido ASC";

        try (Connection conn = DatabaseConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {

            while (rs.next()) {
                lista.add(new Pedido(
                        rs.getInt("idPedido"),
                        rs.getInt("idCliente"),
                        rs.getDate("fecha"),
                        rs.getString("status"),
                        rs.getInt("idProducto"),
                        rs.getInt("cantidad")
                ));
            }
        }
        return lista;
    }


    public List<Pedido> obtenerCliente( int id) throws IOException, SQLException {
        List<Pedido> lista = new ArrayList<>();
        String sql = "SELECT idPedido, idCliente, fecha, status, idProducto, cantidad FROM Pedido WHERE idcliente = ? ";

        try (Connection conn = DatabaseConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setInt(1, id);
            ResultSet rs = ps.executeQuery();


            while (rs.next()) {
                lista.add(new Pedido(
                        rs.getInt("idPedido"),
                        rs.getInt("idCliente"),
                        rs.getDate("fecha"),
                        rs.getString("status"),
                        rs.getInt("idProducto"),
                        rs.getInt("cantidad")
                ));
            }
        }
        return lista;
    }
    public List<Pedido> obtenerPendiente(int id) throws IOException, SQLException {
        List<Pedido> lista = new ArrayList<>();
        String sql = "SELECT idPedido, idCliente, fecha, status, idProducto, cantidad FROM Pedido WHERE idcliente = ? and status = ? ";

        try (Connection conn = DatabaseConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setInt(1, id);
            ps.setString(2,"pendiente" );
            ResultSet rs = ps.executeQuery();

            while (rs.next()) {
                lista.add(new Pedido(
                        rs.getInt("idPedido"),
                        rs.getInt("idCliente"),
                        rs.getDate("fecha"),
                        rs.getString("status"),
                        rs.getInt("idProducto"),
                        rs.getInt("cantidad")
                ));
            }
        }
        return lista;
    }
}
