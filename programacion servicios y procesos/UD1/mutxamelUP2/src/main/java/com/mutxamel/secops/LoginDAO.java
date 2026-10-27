package com.mutxamel.secops;

import com.mutxamel.secops.Login;
import  com.mutxamel.secops.DatabaseConnection;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;
public class LoginDAO {
    // 1. READ (Todos): Consulta estática sin parámetros usando Statement
    public List<Login> obtenerTodos() {
        List<Login> analistas = new ArrayList<>();
        String sql = "SELECT id, user_name, password, created_at FROM login ORDER BY id ASC";
        try {
            Connection con = DatabaseConnection.getConnection();
            try (Statement stmt = con.createStatement();
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
            }
        } catch (SQLException e) {
            System.err.printf("Error SQL en obtenerTodos (%s): %s%n", e.getSQLState(),
                    e.getMessage());
        }
        return analistas;
    }
    // 2. READ (Por Nombre): Consulta parametrizada segura frente a Inyección SQL
    public Login buscarPorUserName(String userName) {
        String sql = "SELECT id, user_name, password, created_at FROM login WHERE user_name = ?";
        try {
            Connection con = DatabaseConnection.getConnection();
            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setString(1, userName); // El parámetro 1 sustituye al primer '?'
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
            }
        } catch (SQLException e) {
            System.err.printf("Error SQL al buscar analista (%s): %s%n", e.getSQLState(),
                    e.getMessage());
        }
        return null; // Si no existe, devolvemos null
    }
    // 3. CREATE: Inserción segura de un nuevo analista con PreparedStatement
    public boolean insertarAnalista(Login nuevo) {
        String sql = "INSERT INTO login (user_name, password) VALUES (?, ?)";
        try {
            Connection con = DatabaseConnection.getConnection();
            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setString(1, nuevo.getUserName());
                ps.setString(2, nuevo.getPassword());
                int filasAfectadas = ps.executeUpdate();
                return filasAfectadas > 0;
            }
        } catch (SQLException e) {
            System.err.printf("Error SQL al insertar analista (%s): %s%n", e.getSQLState(),
                    e.getMessage());
            return false;
        }
    }
}