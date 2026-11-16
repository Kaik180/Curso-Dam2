package com.mutxamel.secops.Proyecto.model;

import java.util.Date;

public class Pedido {
    public int getIdPedido() {
        return idPedido;
    }

    public void setIdPedido(int idPedido) {
        this.idPedido = idPedido;
    }

    public int getIdCliente() {
        return idCliente;
    }

    public void setIdCliente(int idCliente) {
        this.idCliente = idCliente;
    }

    public Date getFecha() {
        return fecha;
    }

    public void setFecha(Date fecha) {
        this.fecha = fecha;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public int getIdProducto() {
        return idProducto;
    }

    public void setIdProducto(int idProducto) {
        this.idProducto = idProducto;
    }

    public int getCantidad() {
        return cantidad;
    }

    public void setCantidad(int cantidad) {
        this.cantidad = cantidad;
    }

    public Pedido(int idPedido, int idCliente, Date fecha, String status, int idProducto, int cantidad) {
        this.idPedido = idPedido;
        this.idCliente = idCliente;
        this.fecha = fecha;
        this.status = status;
        this.idProducto = idProducto;
        this.cantidad = cantidad;
    }

    @Override
    public String toString() {
        return "Pedido [idCliente=" + idCliente + ", idProducto=" + idProducto +
                ", cantidad=" + cantidad + ", fecha=" + fecha + ", status=" + status + "]";
    }

    public Pedido(int idCliente, int idProducto, int cantidad) {
        this.idCliente = idCliente;
        this.idProducto = idProducto;
        this.cantidad = cantidad;
        this.fecha = new java.sql.Date(System.currentTimeMillis()); // Fecha actual en formato SQL Date
        this.status = "pendiente";
    }

    private int idPedido;
    private int idCliente;
    private Date fecha;
    private String status;
    private int idProducto;
    private int cantidad;

}
