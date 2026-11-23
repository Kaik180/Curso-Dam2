package com.mutxamel.secops.Proyecto.model;

import java.sql.Date;

public class Pedido {
    private int idPedido;
    private int idCliente;
    private Date fecha;
    private String status;
    private int idProducto;
    private int cantidad;

    public Pedido() {
    }

    public Pedido(int idCliente, int idProducto, int cantidad) {
        this.idCliente = idCliente;
        this.idProducto = idProducto;
        this.cantidad = cantidad;
        this.fecha = new Date(System.currentTimeMillis());
        this.status = "pendiente";
    }

    public Pedido(int idPedido, int idCliente, Date fecha, String status, int idProducto, int cantidad) {
        this.idPedido = idPedido;
        this.idCliente = idCliente;
        this.fecha = fecha;
        this.status = status;
        this.idProducto = idProducto;
        this.cantidad = cantidad;
    }

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

    @Override
    public String toString() {
        return "Pedido [idPedido=" + idPedido + ", idCliente=" + idCliente + ", fecha=" + fecha +
                ", status=" + status + ", idProducto=" + idProducto + ", cantidad=" + cantidad + "]";
    }
}
