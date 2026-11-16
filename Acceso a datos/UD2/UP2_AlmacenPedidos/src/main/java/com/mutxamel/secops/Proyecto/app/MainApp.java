package com.mutxamel.secops.Proyecto.app;


import com.mutxamel.secops.Proyecto.model.Pedido;
import com.mutxamel.secops.Proyecto.util.DatabaseConnection;
import com.mutxamel.secops.Proyecto.dao.inventarioDao;
import java.io.IOException;
import java.sql.Connection;
import java.sql.SQLException;
import java.util.InputMismatchException;
import java.util.Scanner;
import

public class MainApp {
    public static void main(String[] args) {
        final Scanner teclado = new Scanner(System.in);
        try {
            System.out.print("Introduce el ID del cliente: ");
            int idCliente = teclado.nextInt();

            System.out.print("Introduce el ID del producto: ");
            int idProducto = teclado.nextInt();

            System.out.print("Introduce la cantidad: ");
            int cantidad = teclado.nextInt();

            // Validación básica de entrada
            if (cantidad <= 0) {
                System.out.println("Error: La cantidad debe ser mayor que 0.");
                return;
            }

            Pedido pedido = new Pedido(idCliente, idProducto, cantidad);

            System.out.println("Datos del pedido registrados en memoria: " + pedido);

            try (Connection conn = DatabaseConnection.getConnection()) {
                int stockActualProducto = inventarioDAO.consultarStock(conn, idProducto);

                if (stockActualProducto == -1) {
                    System.out.println("No se puede realizar el pedido: El producto no existe en el inventario.");
                    return;
                }

                if (stockActualProducto < cantidad) {
                    System.out.println("No se puede realizar el pedido: Stock insuficiente (Disponible: " + stockActualProducto + ").");
                    return;
                }

                System.out.println("Stock verificado (" + stockActualProducto + " unidades disponibles).");

                // Aquí llamarás a procesarPedido(pedido, stockActualProducto);
            }

        } catch (InputMismatchException e) {
            System.out.println("Error: Debes introducir números enteros válidos.");
        } catch (
                IOException e) {
            System.out.println("Error al leer el archivo config.properties: " + e.getMessage());
        } catch (
                SQLException e) {
            System.out.println("Error de base de datos al consultar el stock: " + e.getMessage());
        }
    }
}
