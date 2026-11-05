package com.mutxamel.secops.Practica1.model;

public class Usuario {
    public Usuario(String usuario, String clave, int id) {
        this.usuario = usuario;
        this.clave = clave;
        this.id = id;
    }

    private int id;
    private String usuario;
    private String clave;

    public String getUsuario() {
        return usuario;
    }

    public void setUsuario(String usuario) {
        this.usuario = usuario;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getClave() {
        return clave;
    }

    public void setClave(String clave) {
        this.clave = clave;
    }



}
