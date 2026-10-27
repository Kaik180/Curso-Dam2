package com.mutxamel.secops;

import java.sql.Timestamp;
import java.util.Objects;
public class Login {
    private int id;
    private String userName;
    private String password;
    private Timestamp createdAt;
    public Login() {}
    // Constructor para dar de alta un nuevo analista (id y created_at los asigna PostgreSQL)
    public Login(String userName, String password) {
        this.userName = userName;
        this.password = password;
    }
    // Constructor completo para reconstruir (hidratar) el objeto desde un ResultSet
    public Login(int id, String userName, String password, Timestamp createdAt) {
        this.id = id;
        this.userName = userName;
        this.password = password;
        this.createdAt = createdAt;
    }
    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getUserName() { return userName; }
    public void setUserName(String userName) { this.userName = userName; }
    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
    public Timestamp getCreatedAt() { return createdAt; }
    public void setCreatedAt(Timestamp createdAt) { this.createdAt = createdAt; }
    @Override
    public String toString() {
        return String.format("Analista [ID=%d | Usuario=%s | Alta=%s]", id, userName,
                createdAt);
    }
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Login login = (Login) o;
        return id == login.id && Objects.equals(userName, login.userName);
    }
    @Override
    public int hashCode() {
        return Objects.hash(id, userName);
    }
}