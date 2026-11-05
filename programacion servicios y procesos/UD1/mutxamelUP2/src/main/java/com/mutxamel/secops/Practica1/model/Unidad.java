package com.mutxamel.secops.Practica1.model;

public class Unidad {
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getCodigo() {
        return codigo;
    }

    public void setCodigo(String codigo) {
        this.codigo = codigo;
    }

    public String getModelo() {
        return modelo;
    }

    public void setModelo(String modelo) {
        this.modelo = modelo;
    }

    public String getEstado() {
        return estado;
    }

    public void setEstado(String estado) {
        this.estado = estado;
    }

    public int getResponsable_id() {
        return responsable_id;
    }

    public void setResponsable_id(int responsable_id) {
        this.responsable_id = responsable_id;
    }

    public Unidad(int id, String codigo, String modelo, String estado, int responsable_id) {
        this.id = id;
        this.codigo = codigo;
        this.modelo = modelo;
        this.estado = estado;
        this.responsable_id = responsable_id;
    }

    @Override
    public String toString() {
        return "Unidad{" +
                "id=" + id +
                ", codigo='" + codigo + '\'' +
                ", modelo='" + modelo + '\'' +
                ", estado='" + estado + '\'' +
                ", responsable_id=" + responsable_id +
                '}';
    }

    private int id;
    private String codigo;
    private String modelo;
    private String estado;
    private int responsable_id;


}
