package model;

import java.util.Objects;

public class Unidad {
    private int id;
    private String codigo;
    private String modelo;
    private String estado;
    private int responsableId;
    private String responsableUsuario;

    public Unidad() {
    }

    public Unidad(String codigo, String modelo, String estado, int responsableId) {
        this.codigo = codigo;
        this.modelo = modelo;
        this.estado = estado;
        this.responsableId = responsableId;
    }

    public Unidad(int id, String codigo, String modelo, String estado, int responsableId) {
        this.id = id;
        this.codigo = codigo;
        this.modelo = modelo;
        this.estado = estado;
        this.responsableId = responsableId;
    }

    public Unidad(int id, String codigo, String modelo, String estado, int responsableId, String responsableUsuario) {
        this.id = id;
        this.codigo = codigo;
        this.modelo = modelo;
        this.estado = estado;
        this.responsableId = responsableId;
        this.responsableUsuario = responsableUsuario;
    }

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

    public int getResponsableId() {
        return responsableId;
    }

    public void setResponsableId(int responsableId) {
        this.responsableId = responsableId;
    }

    public String getResponsableUsuario() {
        return responsableUsuario;
    }

    public void setResponsableUsuario(String responsableUsuario) {
        this.responsableUsuario = responsableUsuario;
    }

    @Override
    public String toString() {
        String respTexto = (responsableUsuario != null && !responsableUsuario.isBlank())
                ? String.format("%s (ID: %d)", responsableUsuario, responsableId)
                : String.format("ID %d", responsableId);

        return String.format("Unidad [ID=%d | Código=%s | Modelo=%s | Estado=%s | Responsable=%s]",
                id, codigo, modelo, estado, respTexto);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Unidad unidad = (Unidad) o;
        return id == unidad.id && Objects.equals(codigo, unidad.codigo);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, codigo);
    }
}
