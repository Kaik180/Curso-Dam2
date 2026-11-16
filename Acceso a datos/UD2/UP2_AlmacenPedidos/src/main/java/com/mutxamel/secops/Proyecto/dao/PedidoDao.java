package com.mutxamel.secops.Proyecto.dao;


import com.mutxamel.secops.Proyecto.model.Pedido;

import java.util.Scanner;

public class PedidoDao {
    static final Scanner teclado = new Scanner(System.in);
    public void procesarPedido(Pedido pedido, int stockActualProducto) {
    System.out.println("Dime el identificador del cliente");
    int idCliente = teclado.nextInt();
    System.out.println("Dime el identificador del producto");

    }


}
