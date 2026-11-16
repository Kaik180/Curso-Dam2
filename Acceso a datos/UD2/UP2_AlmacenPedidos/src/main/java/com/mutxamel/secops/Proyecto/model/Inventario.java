package com.mutxamel.secops.Proyecto.model;

public class Inventario {
    public int getIdInventario() {
        return idInventario;
    }

    public void setIdInventario(int idInventario) {
        this.idInventario = idInventario;
    }

    public int getStock() {
        return stock;
    }

    public void setStock(int stock) {
        this.stock = stock;
    }

    public int getIdProducto() {
        return idProducto;
    }

    public void setIdProducto(int idProducto) {
        this.idProducto = idProducto;
    }

    public Inventario(int idInventario, int stock, int idProducto) {
        this.idInventario = idInventario;
        this.stock = stock;
        this.idProducto = idProducto;
    }

    @Override
    public String toString() {
        return "Inventario{" +
                "idInventario=" + idInventario +
                ", stock=" + stock +
                ", idProducto=" + idProducto +
                '}';
    }

    private int idInventario;
    private int stock;
    private int idProducto;

}
