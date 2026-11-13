package Practica2.app;

import Practica2.dao.UnidadDAO;
import Practica2.dao.UsuarioDAO;
import Practica2.model.Unidad;
import Practica2.model.Usuario;

import java.io.IOException;
import java.sql.SQLException;
import java.util.List;
import java.util.Scanner;

public class MainApp {

    private static final Scanner scanner = new Scanner(System.in);
    private static final UsuarioDAO usuarioDAO = new UsuarioDAO();
    private static final UnidadDAO unidadDAO = new UnidadDAO();

    public static void main(String[] args) {
        System.out.println("=============================================================");
        System.out.println("   PLD SPACE - SISTEMA DE CONTROL DE ENSAYOS FAMILIA MIURA   ");
        System.out.println("=============================================================\n");

        Usuario usuarioAutenticado = null;

        // Fase 1: Autenticación por consola
        while (usuarioAutenticado == null) {
            System.out.println("--- Inicio de Sesión de Personal Técnico ---");
            System.out.print("Nombre de usuario: ");
            String usuario = scanner.nextLine().trim();

            System.out.print("Contraseña: ");
            String clave = scanner.nextLine().trim();

            if (usuario.equalsIgnoreCase("salir") || clave.equalsIgnoreCase("salir")) {
                System.out.println("Saliendo de la aplicación...");
                return;
            }

            try {
                usuarioAutenticado = usuarioDAO.autenticar(usuario, clave);

                if (usuarioAutenticado == null) {
                    System.out.println("\n[ACCESO DENEGADO]: Credenciales incorrectas. Verifique el usuario y la clave.");
                    System.out.println("(Escriba 'salir' para finalizar o vuelva a intentarlo)\n");
                } else {
                    System.out.println("\n[ACCESO CONCEDIDO]: Bienvenido/a, " + usuarioAutenticado.getUsuario() +
                                       " (ID: " + usuarioAutenticado.getId() + ")\n");
                }

            } catch (IOException e) {
                System.err.println("\n[ERROR DE CONFIGURACIÓN]: No se pudo cargar 'config.properties'.");
                System.err.println("Detalle: " + e.getMessage());
                System.err.println("Asegúrese de que el archivo config.properties existe en la raíz del proyecto.\n");
                return;
            } catch (SQLException e) {
                System.err.println("\n[ERROR DE BASE DE DATOS]: Fallo de conexión o consulta en PostgreSQL.");
                System.err.println("Código SQLState: " + e.getSQLState());
                System.err.println("Mensaje: " + e.getMessage());
                System.err.println("Compruebe que PostgreSQL está en ejecución y la base de datos 'pldspace_lab' creada.\n");
                return;
            }
        }

        // FASE 2: Menú de gestión de unidades MIURA
        boolean salir = false;
        while (!salir) {
            mostrarMenu();
            System.out.print("Seleccione una opción: ");
            String opcionStr = scanner.nextLine().trim();

            switch (opcionStr) {
                case "1": listarUnidades();
                case "2": buscarUnidadPorId();
                case "3": insertarNuevaUnidad();
                case "4": modificarEstadoUnidad();
                case "5": eliminarUnidad();
                case "6":iniciarCampaniaPruebas();
                case "0": {
                    System.out.println("\nCerrando sesión de " + usuarioAutenticado.getUsuario() + ". ¡Hasta pronto!");
                    salir = true;
                }
                default: System.out.println("\nOpción no válida. Por favor, seleccione un número del menú.");
            }
        }
    }

    private static void mostrarMenu() {
        System.out.println("\n-------------------------------------------------------------");
        System.out.println("        MENÚ PRINCIPAL - GESTIÓN DE UNIDADES MIURA          ");
        System.out.println("-------------------------------------------------------------");
        System.out.println("1. Listar todas las unidades (código, modelo, estado y responsable)");
        System.out.println("2. Buscar una unidad por su identificador");
        System.out.println("3. Insertar una nueva unidad (asignándola a un responsable)");
        System.out.println("4. Modificar el estado de una unidad existente");
        System.out.println("5. Eliminar una unidad por su identificador");
        System.out.println("6. Iniciar una campaña conjunta de pruebas (Transacción con rollback/commit)");
        System.out.println("0. Salir del programa");
        System.out.println("-------------------------------------------------------------");
    }

    // Opción 1: Listar todas las unidades
    private static void listarUnidades() {
        System.out.println("\n=== INVENTARIO COMPLETO DE UNIDADES MIURA ===");
        try {
            List<Unidad> unidades = unidadDAO.obtenerTodas();
            if (unidades.isEmpty()) {
                System.out.println("No hay unidades registradas en la base de datos.");
            } else {
                for (Unidad u : unidades) {
                    System.out.println(u);
                }
            }
        } catch (IOException | SQLException e) {
            mostrarErrorBD(e);
        }
    }

    // Opción 2: Buscar unidad por identificador
    private static void buscarUnidadPorId() {
        System.out.println("\n=== BÚSQUEDA DE UNIDAD ===");
        System.out.print("Introduzca el ID numérico de la unidad (o 'c' para buscar por código): ");
        String entrada = scanner.nextLine().trim();

        try {
            Unidad unidad;
            if (entrada.equalsIgnoreCase("c")) {
                System.out.print("Introduzca el código exacto (ej. M1-AULA01): ");
                String cod = scanner.nextLine().trim();
                unidad = unidadDAO.buscarPorCodigo(cod);
            } else {
                int id = Integer.parseInt(entrada);
                unidad = unidadDAO.buscarPorId(id);
            }

            if (unidad != null) {
                System.out.println("✓ Unidad localizada:");
                System.out.println("  " + unidad);
            } else {
                System.out.println("✗ No se encontró ninguna unidad con el identificador indicado.");
            }
        } catch (NumberFormatException e) {
            System.out.println("Identificador no válido. Debe ser un número entero.");
        } catch (IOException | SQLException e) {
            mostrarErrorBD(e);
        }
    }

    // Opción 3: Insertar nueva unidad
    private static void insertarNuevaUnidad() {
        System.out.println("\n=== REGISTRO DE NUEVA UNIDAD MIURA ===");
        try {
            System.out.print("Código de la unidad (ej: M5-AULA04): ");
            String codigo = scanner.nextLine().trim();

            if (codigo.isBlank()) {
                System.out.println("El código no puede estar vacío.");
                return;
            }

            System.out.println("Modelos admitidos: 1) MIURA 1 | 2) MIURA 5");
            System.out.print("Seleccione modelo (1 o 2, o escriba el nombre): ");
            String modOpc = scanner.nextLine().trim();
            String modelo = switch (modOpc) {
                case "1" -> "MIURA 1";
                case "2" -> "MIURA 5";
                default -> modOpc.toUpperCase();
            };

            System.out.println("Estados válidos: 1) PLANIFICADA | 2) INTEGRACION | 3) EN_ENSAYOS | 4) REVISION");
            System.out.print("Seleccione estado (1-4, o escriba el nombre): ");
            String estOpc = scanner.nextLine().trim();
            String estado = switch (estOpc) {
                case "1" -> "PLANIFICADA";
                case "2" -> "INTEGRACION";
                case "3" -> "EN_ENSAYOS";
                case "4" -> "REVISION";
                default -> estOpc.toUpperCase();
            };

            // Mostrar usuarios existentes para asignar responsable válido
            System.out.println("Técnicos responsables disponibles:");
            List<Usuario> usuarios = usuarioDAO.obtenerTodos();
            for (Usuario u : usuarios) {
                System.out.printf("  [ID: %d] %s%n", u.getId(), u.getUsuario());
            }

            System.out.print("ID del responsable técnico: ");
            int responsableId = Integer.parseInt(scanner.nextLine().trim());

            if (!usuarioDAO.existePorId(responsableId)) {
                System.out.println("✗ Error: El ID de responsable " + responsableId + " no existe.");
                return;
            }

            Unidad nueva = new Unidad(codigo, modelo, estado, responsableId);
            boolean exito = unidadDAO.insertar(nueva);

            if (exito) {
                System.out.println("✓ Unidad registrada con éxito en el sistema.");
            } else {
                System.out.println("✗ No se pudo registrar la unidad.");
            }

        } catch (NumberFormatException e) {
            System.out.println("El ID del responsable debe ser numérico.");
        } catch (IOException | SQLException e) {
            mostrarErrorBD(e);
        }
    }

    // Opción 4: Modificar estado de una unidad
    private static void modificarEstadoUnidad() {
        System.out.println("\n=== MODIFICAR ESTADO DE UNIDAD ===");
        try {
            System.out.print("ID de la unidad a modificar: ");
            int id = Integer.parseInt(scanner.nextLine().trim());

            Unidad actual = unidadDAO.buscarPorId(id);
            if (actual == null) {
                System.out.println("✗ No existe ninguna unidad con el ID " + id);
                return;
            }

            System.out.println("Unidad actual: " + actual);
            System.out.println("Nuevos estados posibles: 1) PLANIFICADA | 2) INTEGRACION | 3) EN_ENSAYOS | 4) REVISION");
            System.out.print("Seleccione nuevo estado (1-4): ");
            String opc = scanner.nextLine().trim();
            String nuevoEstado = switch (opc) {
                case "1" -> "PLANIFICADA";
                case "2" -> "INTEGRACION";
                case "3" -> "EN_ENSAYOS";
                case "4" -> "REVISION";
                default -> opc.toUpperCase();
            };

            boolean exito = unidadDAO.modificarEstado(id, nuevoEstado);
            if (exito) {
                System.out.println("✓ Estado actualizado correctamente a '" + nuevoEstado + "'.");
            } else {
                System.out.println("✗ No se pudo actualizar el estado de la unidad.");
            }

        } catch (NumberFormatException e) {
            System.out.println("El identificador debe ser numérico.");
        } catch (IOException | SQLException e) {
            mostrarErrorBD(e);
        }
    }

    // Opción 5: Eliminar unidad por identificador
    private static void eliminarUnidad() {
        System.out.println("\n=== ELIMINAR UNIDAD ===");
        try {
            System.out.print("ID de la unidad a eliminar: ");
            int id = Integer.parseInt(scanner.nextLine().trim());

            Unidad actual = unidadDAO.buscarPorId(id);
            if (actual == null) {
                System.out.println("✗ No existe ninguna unidad con el ID " + id);
                return;
            }

            System.out.println("Unidad a eliminar: " + actual);
            System.out.print("¿Confirma la eliminación permanente? (s/N): ");
            String confirmacion = scanner.nextLine().trim();

            if (confirmacion.equalsIgnoreCase("s")) {
                boolean exito = unidadDAO.eliminarPorId(id);
                if (exito) {
                    System.out.println("✓ Unidad eliminada correctamente de la base de datos.");
                } else {
                    System.out.println("✗ No se pudo eliminar la unidad.");
                }
            } else {
                System.out.println("Operación de eliminación cancelada.");
            }

        } catch (NumberFormatException e) {
            System.out.println("El identificador debe ser un número entero.");
        } catch (IOException | SQLException e) {
            mostrarErrorBD(e);
        }
    }

    // Opción 6: Campaña conjunta de pruebas (Transacción con rollback y commit)
    private static void iniciarCampaniaPruebas() {

    }
    //Mostrar el tipo de error que sale en su caso.
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
