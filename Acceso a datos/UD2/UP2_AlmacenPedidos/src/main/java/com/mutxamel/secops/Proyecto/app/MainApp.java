package com.mutxamel.secops.Proyecto.app;

import com.mutxamel.secops.Proyecto.dao.PedidoDao;
import com.mutxamel.secops.Proyecto.dao.inventarioDao;
import com.mutxamel.secops.Proyecto.model.Pedido;
import com.mutxamel.secops.Proyecto.util.DatabaseConnection;

import java.io.IOException;
import java.sql.Connection;
import java.sql.SQLException;
import java.util.InputMismatchException;
import java.util.Scanner;

public class MainApp {

    private static final Scanner teclado = new Scanner(System.in);
    private static final inventarioDao inventarioDAO = new inventarioDao();
    private static final PedidoDao pedidoDAO = new PedidoDao();

    public static void main(String[] args) {
        System.out.println("=============================================================");
        System.out.println("  PROYECTO UP2: GESTIÓN DE ALMACÉN Y PEDIDOS (UP2_AlmacenPedidos)");
        System.out.println("=============================================================\n");

        boolean continuar = true;

        while (continuar) {
            try {
                // Paso 1: Solicitar los datos del pedido por consola
                System.out.print("Introduce el ID del cliente: ");
                int idCliente = teclado.nextInt();

                System.out.print("Introduce el ID del producto: ");
                int idProducto = teclado.nextInt();

                System.out.print("Introduce la cantidad solicitada: ");
                int cantidad = teclado.nextInt();

                if (cantidad <= 0) {
                    System.out.println("✗ Error: La cantidad debe ser mayor que 0.\n");
                    continue;
                }

                // Creación del objeto pedido en memoria con fecha actual y estado inicial 'pendiente'
                Pedido pedido = new Pedido(idCliente, idProducto, cantidad);
                System.out.println("\n-> Datos del pedido registrados: " + pedido);

                // Paso 2: Consultar en la base de datos el stock actual antes de llamar a procesarPedido()
                try (Connection conn = DatabaseConnection.getConnection()) {
                    int stockActualProducto = inventarioDAO.consultarStock(conn, idProducto);

                    if (stockActualProducto == -1) {
                        System.out.println("✗ No se puede realizar el pedido: El producto con ID " + idProducto + " no existe en el inventario.\n");
                        continue;
                    }

                    if (stockActualProducto < cantidad) {
                        System.out.println("✗ No se puede realizar el pedido: Stock insuficiente.");
                        System.out.println("  Stock disponible: " + stockActualProducto + " | Cantidad solicitada: " + cantidad + "\n");
                        continue;
                    }

                    System.out.println("-> Stock verificado: " + stockActualProducto + " unidades disponibles en inventario.");

                    // Llamada al método obligatorio para procesar el pedido dentro de la transacción
                    pedidoDAO.procesarPedido(pedido, stockActualProducto);
                }

            } catch (InputMismatchException e) {
                System.out.println("✗ Error: Debes introducir números enteros válidos.");
                teclado.nextLine(); // Limpiar el buffer
            } catch (IOException e) {
                System.err.println("✗ Error al leer el archivo config.properties: " + e.getMessage());
            } catch (SQLException e) {
                System.err.println("✗ Error de base de datos al consultar el stock: " + e.getMessage());
            }

            System.out.print("\n¿Deseas procesar otro pedido? (s/N): ");
            String respuesta = teclado.next();
            if (!respuesta.equalsIgnoreCase("s")) {
                continuar = false;
                System.out.println("\nPrograma finalizado.");
            }
            System.out.println();
        }
    }
}
