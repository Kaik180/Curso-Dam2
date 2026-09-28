package es.iesmutxamel.ludoteca;

import java.util.ArrayList;
import java.util.Locale;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        Catalogo catalogo = new Catalogo();

        // Añadimos los dos videojuegos de la tarea anterior
        catalogo.agregarVideojuego(new Videojuego(100, "The witcher", "pc", 20.00, 7));
        catalogo.agregarVideojuego(new Videojuego(101, "Órbita", "pc", 19.95, 7));

        Scanner scanner = new Scanner(System.in);
        int opcion = -1;

        do {
            mostrarMenu();
            opcion = leerOpcionMenu(scanner);

            switch (opcion) {
                case 1:
                    mostrarTodosLosVideojuegos(catalogo);
                    break;
                case 2:
                    agregarVideojuego(scanner, catalogo);
                    break;
                case 3:
                    mostrarResumenCatalogo(catalogo);
                    break;
                case 4:
                    consultarPocasUnidades(scanner, catalogo);
                    break;
                case 0:
                    System.out.println("¡Gracias por utilizar la aplicación de Ludoteca IES! ¡Hasta pronto!");
                    break;
                default:
                    System.out.println("Error: Opción no válida. Por favor, selecciona una opción entre 0 y 4.");
                    break;
            }
        } while (opcion != 0);
    }

    private static void mostrarMenu() {
        System.out.println();
        System.out.println("LUDOTECA IES");
        System.out.println("1. Mostrar todos los videojuegos");
        System.out.println("2. Añadir un videojuego");
        System.out.println("3. Mostrar un resumen del catálogo");
        System.out.println("4. Consultar videojuegos con pocas unidades");
        System.out.println("0. Salir");
        System.out.print(">> Selecciona una opción: ");
    }

    private static int leerOpcionMenu(Scanner scanner) {
        String linea = scanner.nextLine().trim();
        try {
            return Integer.parseInt(linea);
        } catch (NumberFormatException e) {
            return -1; // Opción no válida si introduce texto
        }
    }

    private static void mostrarTodosLosVideojuegos(Catalogo catalogo) {
        ArrayList<Videojuego> lista = catalogo.obtenerVideojuegos();
        if (lista.isEmpty()) {
            System.out.println("El catálogo está vacío.");
        } else {
            System.out.println("--- LISTA DE VIDEOJUEGOS ---");
            for (Videojuego v : lista) {
                System.out.println(v);
            }
        }
    }

    private static void agregarVideojuego(Scanner scanner, Catalogo catalogo) {
        System.out.println("--- AÑADIR UN VIDEOJUEGO ---");

        // 1. Identificador
        int id = -1;
        while (true) {
            System.out.print("Introduce el identificador (o 'cancelar' para volver): ");
            String input = scanner.nextLine().trim();
            if (input.equalsIgnoreCase("cancelar")) {
                System.out.println("Operación cancelada. Volviendo al menú principal.");
                return;
            }
            try {
                id = Integer.parseInt(input);
                if (id < 0) {
                    System.out.println("Error: El identificador no puede tener un valor negativo. Inténtalo de nuevo.");
                    continue;
                }
                if (catalogo.buscarPorId(id) != null) {
                    System.out.println("Error: Ya existe un videojuego con el identificador " + id + ". Inténtalo con otro número.");
                    continue;
                }
                break;
            } catch (NumberFormatException e) {
                System.out.println("Error: Se ha introducido texto cuando se esperaba un número. Inténtalo de nuevo.");
            }
        }

        // 2. Título
        String titulo = "";
        while (true) {
            System.out.print("Introduce el título: ");
            titulo = scanner.nextLine().trim();
            if (titulo.isEmpty()) {
                System.out.println("Error: El título no puede estar vacío. Inténtalo de nuevo.");
                continue;
            }
            break;
        }

        // 3. Plataforma
        String plataforma = "";
        while (true) {
            System.out.print("Introduce la plataforma: ");
            plataforma = scanner.nextLine().trim();
            if (plataforma.isEmpty()) {
                System.out.println("Error: La plataforma no puede estar vacía. Inténtalo de nuevo.");
                continue;
            }
            break;
        }

        // 4. Precio
        double precio = -1.0;
        while (true) {
            System.out.print("Introduce el precio: ");
            String input = scanner.nextLine().trim().replace(',', '.');
            try {
                precio = Double.parseDouble(input);
                if (precio < 0) {
                    System.out.println("Error: El precio no puede tener un valor negativo. Inténtalo de nuevo.");
                    continue;
                }
                break;
            } catch (NumberFormatException e) {
                System.out.println("Error: Se ha introducido texto cuando se esperaba un número decimal. Inténtalo de nuevo.");
            }
        }

        // 5. Stock
        int stock = -1;
        while (true) {
            System.out.print("Introduce el stock: ");
            String input = scanner.nextLine().trim();
            try {
                stock = Integer.parseInt(input);
                if (stock < 0) {
                    System.out.println("Error: El stock no puede tener un valor negativo. Inténtalo de nuevo.");
                    continue;
                }
                break;
            } catch (NumberFormatException e) {
                System.out.println("Error: Se ha introducido texto cuando se esperaba un número entero. Inténtalo de nuevo.");
            }
        }

        Videojuego nuevo = new Videojuego(id, titulo, plataforma, precio, stock);
        boolean exito = catalogo.agregarVideojuego(nuevo);
        if (exito) {
            System.out.println("Videojuego añadido correctamente al catálogo.");
        } else {
            System.out.println("Error: No se pudo añadir el videojuego.");
        }
    }

    private static void mostrarResumenCatalogo(Catalogo catalogo) {
        System.out.println("--- RESUMEN DEL CATÁLOGO ---");
        System.out.println("• Número de videojuegos diferentes: " + catalogo.obtenerCantidad());
        System.out.println("• Número total de unidades disponibles: " + catalogo.obtenerTotalUnidades());
        System.out.printf(Locale.ROOT, "• Valor total del stock: %.2f €%n", catalogo.obtenerValorTotalStock());
    }

    private static void consultarPocasUnidades(Scanner scanner, Catalogo catalogo) {
        System.out.println("--- CONSULTAR VIDEOJUEGOS CON POCAS UNIDADES ---");
        int limite = -1;
        while (true) {
            System.out.print("Introduce la cantidad máxima de unidades a consultar (o 'cancelar' para volver): ");
            String input = scanner.nextLine().trim();
            if (input.equalsIgnoreCase("cancelar")) {
                System.out.println("Operación cancelada. Volviendo al menú principal.");
                return;
            }
            try {
                limite = Integer.parseInt(input);
                if (limite < 0) {
                    System.out.println("Error: El límite de stock introducido no puede ser negativo. Inténtalo de nuevo.");
                    continue;
                }
                break;
            } catch (NumberFormatException e) {
                System.out.println("Error: Se ha introducido texto cuando se esperaba un número. Inténtalo de nuevo.");
            }
        }

        ArrayList<Videojuego> pocos = catalogo.buscarPorStockMaximo(limite);
        if (pocos.isEmpty()) {
            System.out.println("No hay ningún videojuego con un stock de " + limite + " unidades o menos.");
        } else {
            System.out.println("Videojuegos con stock menor o igual a " + limite + ":");
            for (Videojuego v : pocos) {
                System.out.println(v);
            }
        }
    }
}
