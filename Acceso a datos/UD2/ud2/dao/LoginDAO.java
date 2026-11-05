package com.mutxamel.secops.Practica1.ud2.dao;



import com.mutxamel.secops.Practica1.ud2.model.Login;
import com.mutxamel.secops.Practica1.ud2.util.DatabaseConnection;

import java.io.IOException;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class LoginDAO {

    // 1. READ (Todos): Consulta estática sin parámetros usando Statement
    public List<Login> obtenerTodos() {
        List<Login> analistas = new ArrayList<>();
        String sql = "SELECT id, user_name, password, created_at FROM login ORDER BY id ASC";
        try (Connection con = DatabaseConnection.getConnection();
             Statement stmt = con.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                Login a = new Login(
                        rs.getInt("id"),
                        rs.getString("user_name"),
                        rs.getString("password"),
                        rs.getTimestamp("created_at")
                );
                analistas.add(a);
            }
        } catch (IOException | SQLException e) {
            System.err.printf("Error en obtenerTodos (%s): %s%n",
                    (e instanceof SQLException) ? ((SQLException) e).getSQLState() : "IO", e.getMessage());
        }
        return analistas;
    }

    // 2. READ (Por Nombre): Consulta parametrizada segura frente a Inyección SQL
    public Login buscarPorUserName(String userName) {
        String sql = "SELECT id, user_name, password, created_at FROM login WHERE user_name = ?";
        try (Connection con = DatabaseConnection.getConnection();
             PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setString(1, userName);
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    return new Login(
                            rs.getInt("id"),
                            rs.getString("user_name"),
                            rs.getString("password"),
                            rs.getTimestamp("created_at")
                    );
                }
            }
        } catch (IOException | SQLException e) {
            System.err.printf("Error al buscar analista (%s): %s%n",
                    (e instanceof SQLException) ? ((SQLException) e).getSQLState() : "IO", e.getMessage());
        }
        return null;
    }

    // 3. CREATE: Inserción segura de un nuevo analista con PreparedStatement
    public boolean insertarAnalista(Login nuevo) {
        String sql = "INSERT INTO login (user_name, password) VALUES (?, ?)";
        try (Connection con = DatabaseConnection.getConnection();
             PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setString(1, nuevo.getUserName());
            ps.setString(2, nuevo.getPassword());
            int filasAfectadas = ps.executeUpdate();
            return filasAfectadas > 0;
        } catch (IOException | SQLException e) {
            System.err.printf("Error al insertar analista (%s): %s%n",
                    (e instanceof SQLException) ? ((SQLException) e).getSQLState() : "IO", e.getMessage());
            return false;
        }
    }
}
