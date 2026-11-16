package Proyecto.app.model;

import java.util.Date;

public class Envio {
    public int getIdEnvio() {
        return idEnvio;
    }

    public void setIdEnvio(int idEnvio) {
        this.idEnvio = idEnvio;
    }

    public Date getFechaEnvio() {
        return fechaEnvio;
    }

    public void setFechaEnvio(Date fechaEnvio) {
        this.fechaEnvio = fechaEnvio;
    }

    public int getIdProducto() {
        return idProducto;
    }

    public void setIdProducto(int idProducto) {
        this.idProducto = idProducto;
    }

    public Envio(int idEnvio, Date fechaEnvio, int idProducto) {
        this.idEnvio = idEnvio;
        this.fechaEnvio = fechaEnvio;
        this.idProducto = idProducto;
    }

    @Override
    public String toString() {
        return "Envio{" +
                "idEnvio=" + idEnvio +
                ", fechaEnvio=" + fechaEnvio +
                ", idProducto=" + idProducto +
                '}';
    }

    private int idEnvio;
    private Date fechaEnvio;
    private int idProducto;
}
