package Practica2.dao;

import Practica2.model.Usuario;
import Practica2.util.DatabaseConnection;

import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class UsuarioDAO {


    public Usuario autenticar(String usuario, String clave) throws IOException, SQLException {
        String sql = "SELECT id, usuario, clave FROM usuarios WHERE usuario = ? AND clave = ?";

        try (Connection con = DatabaseConnection.getConnection();
             PreparedStatement ps = con.prepareStatement(sql)) {

            ps.setString(1, usuario);
            ps.setString(2, clave);

            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    return new Usuario(
                            rs.getInt("id"),
                            rs.getString("usuario"),
                            rs.getString("clave")
                    );
                }
            }
        }
        return null; // Credenciales incorrectas
    }


     // Comprueba si existe un usuario con un ID específico.

    public boolean existePorId(int id) throws IOException, SQLException {
        String sql = "SELECT 1 FROM usuarios WHERE id = ?";
        try (Connection con = DatabaseConnection.getConnection();
             PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setInt(1, id);
            try (ResultSet rs = ps.executeQuery()) {
                return rs.next();
            }
        }
    }


     //Lista todos los usuarios técnicos registrados.

    public List<Usuario> obtenerTodos() throws IOException, SQLException {
        List<Usuario> lista = new ArrayList<>();
        String sql = "SELECT id, usuario, clave FROM usuarios ORDER BY id ASC";
        try (Connection con = DatabaseConnection.getConnection();
             PreparedStatement ps = con.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                lista.add(new Usuario(
                        rs.getInt("id"),
                        rs.getString("usuario"),
                        rs.getString("clave")
                ));
            }
        }
        return lista;
    }
}
