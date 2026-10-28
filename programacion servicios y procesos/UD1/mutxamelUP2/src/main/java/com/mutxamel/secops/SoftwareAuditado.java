package com.mutxamel.secops;

public class SoftwareAuditado {
    private int codigo;
    private String nombre;
    private Integer nivelExposicion; // Usamos Integer (Wrapper) para soportar posibles NULLde forma segura
    public SoftwareAuditado() {}
    public SoftwareAuditado(String nombre, Integer nivelExposicion) {
        this.nombre = nombre;
        this.nivelExposicion = nivelExposicion;
    }
    public SoftwareAuditado(int codigo, String nombre, Integer nivelExposicion) {
        this.codigo = codigo;
        this.nombre = nombre;
        this.nivelExposicion = nivelExposicion;
    }
    public int getCodigo() { return codigo; }
    public void setCodigo(int codigo) { this.codigo = codigo; }
    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }
    public Integer getNivelExposicion() { return nivelExposicion; }
    public void setNivelExposicion(Integer nivelExposicion) { this.nivelExposicion =
            nivelExposicion; }
    @Override
    public String toString() {
        String riesgoTexto = (nivelExposicion != null) ? nivelExposicion + "/5" : "SIN EVALUAR (NULL)";
        return String.format("Software [Código=%d | Nombre=%s | Riesgo=%s]", codigo, nombre,
                riesgoTexto);
    }
}