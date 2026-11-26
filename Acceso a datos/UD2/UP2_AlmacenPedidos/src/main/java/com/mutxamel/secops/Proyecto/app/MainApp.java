package com.mutxamel.secops.Proyecto.app;

import com.mutxamel.secops.Proyecto.dao.PedidoDao;
import com.mutxamel.secops.Proyecto.dao.inventarioDao;
import com.mutxamel.secops.Proyecto.model.Pedido;
import com.mutxamel.secops.Proyecto.util.DatabaseConnection;

import java.io.IOException;
import java.sql.Connection;
import java.sql.SQLException;
import java.util.List;
import java.util.Scanner;

public class MainApp {

    private static final Scanner teclado = new Scanner(System.in);
    private static final inventarioDao inventarioDAO = new inventarioDao();
    private static final PedidoDao pedidoDAO = new PedidoDao();

    public static void main(String[] args) {
        System.out.println("=============================================================");
        System.out.println("  PROYECTO UP2: GESTIÓN DE ALMACÉN Y PEDIDOS (UP2_AlmacenPedidos)");
        System.out.println("=============================================================");

        boolean salir = false;

        while (!salir) {
            mostrarMenu();
            System.out.print("Seleccione una opción: ");
            String opcion = teclado.nextLine().trim();

            switch (opcion) {
                case "1" -> procesarNuevoPedido();
                case "2" -> consultarPedidosPorEstado();
                case "3" -> consultarPedidosPorProducto();
                case "4" -> listarTodosLosPedidos();
                case "5" -> consultarStockProducto();
                case "0" -> {
                    System.out.println("\nPrograma finalizado. ¡Hasta pronto!");
                    salir = true;
                }
                default -> System.out.println("\n✗ Opción no válida. Por favor, introduzca un número del menú.");
            }
        }
    }

    private static void mostrarMenu() {
        System.out.println("\n-------------------------------------------------------------");
        System.out.println("               MENÚ PRINCIPAL - ALMACÉN DE PEDIDOS           ");
        System.out.println("-------------------------------------------------------------");
        System.out.println("1. Procesar un nuevo pedido (Transacción con regla de stock >= 10)");
        System.out.println("2. Consultar pedidos por estado (MODELO A - pendiente, enviado)");
        System.out.println("3. Consultar pedidos por producto (MODELO B - por idProducto)");
        System.out.println("4. Listar todos los pedidos registrados");
        System.out.println("5. Consultar stock disponible de un producto");
        System.out.println("0. Salir");
        System.out.println("-------------------------------------------------------------");
    }

    private static void procesarNuevoPedido() {
        System.out.println("\n=== REGISTRAR Y PROCESAR NUEVO PEDIDO ===");
        try {
            System.out.print("Introduce el ID del cliente: ");
            int idCliente = Integer.parseInt(teclado.nextLine().trim());

            System.out.print("Introduce el ID del producto: ");
            int idProducto = Integer.parseInt(teclado.nextLine().trim());

            System.out.print("Introduce la cantidad solicitada: ");
            int cantidad = Integer.parseInt(teclado.nextLine().trim());

            if (cantidad <= 0) {
                System.out.println("✗ Error: La cantidad debe ser mayor que 0.");
                return;
            }

            Pedido pedido = new Pedido(idCliente, idProducto, cantidad);
            System.out.println("-> Datos del pedido registrados en memoria: " + pedido);

            try (Connection conn = DatabaseConnection.getConnection()) {
                int stockActualProducto = inventarioDAO.consultarStock(conn, idProducto);

                if (stockActualProducto == -1) {
                    System.out.println("✗ No se puede realizar el pedido: El producto con ID " + idProducto + " no existe en el inventario.");
                    return;
                }

                if (stockActualProducto < cantidad) {
                    System.out.println("✗ No se puede realizar el pedido: Stock insuficiente.");
                    System.out.println("  Stock disponible: " + stockActualProducto + " | Cantidad solicitada: " + cantidad);
                    return;
                }

                System.out.println("-> Stock verificado: " + stockActualProducto + " unidades disponibles en inventario.");

                pedidoDAO.procesarPedido(pedido, stockActualProducto);
            }

        } catch (NumberFormatException e) {
            System.out.println("✗ Error: Debe introducir números enteros válidos.");
        } catch (IOException e) {
            System.err.println("✗ Error al leer config.properties: " + e.getMessage());
        } catch (SQLException e) {
            System.err.println("✗ Error de base de datos al consultar stock: " + e.getMessage());
        }
    }

    private static void consultarPedidosPorEstado() {
        System.out.println("\n=== CONSULTA DE PEDIDOS POR ESTADO (MODELO A) ===");
        System.out.println("Estados habituales: 1) pendiente | 2) enviado");
        System.out.print("Introduce el estado a consultar (1 o 2, o escribe el nombre): ");
        String entrada = teclado.nextLine().trim();

        String status = switch (entrada) {
            case "1" -> "pendiente";
            case "2" -> "enviado";
            default -> entrada.toLowerCase();
        };

        if (status.isBlank()) {
            System.out.println("✗ Debe introducir un estado válido.");
            return;
        }

        try {
            List<Pedido> pedidos = pedidoDAO.buscarPorEstado(status);
            if (pedidos.isEmpty()) {
                System.out.println("No existen pedidos que cumplan la condición para el estado '" + status + "'.");
            } else {
                System.out.printf("%nPedidos encontrados con estado '%s' (%d):%n", status, pedidos.size());
                for (Pedido p : pedidos) {
                    System.out.printf("  - ID Pedido: %-4d | Cliente: %-4d | Fecha: %s | Producto: %-4d | Cantidad: %-4d | Estado: %s%n",
                            p.getIdPedido(), p.getIdCliente(), p.getFecha(), p.getIdProducto(), p.getCantidad(), p.getStatus());
                }
            }
        } catch (IOException | SQLException e) {
            mostrarErrorBD(e);
        }
    }

    private static void consultarPedidosPorProducto() {
        System.out.println("\n=== CONSULTA DE PEDIDOS POR PRODUCTO (MODELO B) ===");
        System.out.print("Introduce el ID del producto: ");
        try {
            int idProducto = Integer.parseInt(teclado.nextLine().trim());
            List<Pedido> pedidos = pedidoDAO.buscarPorProducto(idProducto);

            if (pedidos.isEmpty()) {
                System.out.println("No existen pedidos registrados para el producto con ID " + idProducto + ".");
            } else {
                System.out.printf("%nPedidos encontrados para el producto ID %d (%d):%n", idProducto, pedidos.size());
                for (Pedido p : pedidos) {
                    System.out.printf("  - ID Pedido: %-4d | Cliente: %-4d | Fecha: %s | Cantidad: %-4d | Estado: %s%n",
                            p.getIdPedido(), p.getIdCliente(), p.getFecha(), p.getCantidad(), p.getStatus());
                }
            }
        } catch (NumberFormatException e) {
            System.out.println("✗ Error: El ID del producto debe ser un número entero.");
        } catch (IOException | SQLException e) {
            mostrarErrorBD(e);
        }
    }

    private static void listarTodosLosPedidos() {
        System.out.println("\n=== LISTADO GENERAL DE PEDIDOS ===");
        try {
            List<Pedido> pedidos = pedidoDAO.obtenerTodos();
            if (pedidos.isEmpty()) {
                System.out.println("No hay pedidos registrados en la base de datos.");
            } else {
                System.out.printf("Total de pedidos registrados: %d%n", pedidos.size());
                for (Pedido p : pedidos) {
                    System.out.println("  " + p);
                }
            }
        } catch (IOException | SQLException e) {
            mostrarErrorBD(e);
        }
    }

    private static void consultarStockProducto() {
        System.out.println("\n=== CONSULTA DE STOCK EN INVENTARIO ===");
        System.out.print("Introduce el ID del producto: ");
        try {
            int idProducto = Integer.parseInt(teclado.nextLine().trim());
            int stock = inventarioDAO.consultarStock(idProducto);

            if (stock == -1) {
                System.out.println("✗ El producto con ID " + idProducto + " no existe en el inventario.");
            } else {
                System.out.printf("-> Producto ID %d: Stock actual en inventario = %d unidades.%n", idProducto, stock);
            }
        } catch (NumberFormatException e) {
            System.out.println("✗ Error: El ID del producto debe ser numérico.");
        } catch (IOException | SQLException e) {
            mostrarErrorBD(e);
        }
    }

    private static void mostrarErrorBD(Exception e) {
        System.err.println("\n[ERROR EN LA OPERACIÓN]:");
        if (e instanceof SQLException sqlEx) {
            System.err.println("  Mensaje SQL: " + sqlEx.getMessage());
            System.err.println("  SQLState: " + sqlEx.getSQLState());
        } else {
            System.err.println("  Mensaje: " + e.getMessage());
        }
    }
}
