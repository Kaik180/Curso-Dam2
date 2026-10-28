import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.util.Scanner;

public class ModificarTexto {

    public static void main(String[] args) {
        String nombreFichero = "texto.txt";
        File archivo = new File(nombreFichero);

        // Si el archivo no existe o está vacío, creamos un archivo con texto de prueba
        if (!archivo.exists() || archivo.length() == 0) {
            try (FileWriter fw = new FileWriter(archivo)) {
                fw.write("Java es un lenguaje de programacion orientado a objetos.\r\n" +
                         "En este ejercicio usamos ficheros con java para aprender.\r\n" +
                         "El profesor nos pide buscar una palabra en java y cambiarla.\r\n" +
                         "Esta linea final no contiene la palabra clave.\r\n");
                System.out.println("Fichero 'texto.txt' creado con texto de prueba.\n");
            } catch (IOException e) {
                System.out.println("Error al crear el fichero de prueba: " + e.getMessage());
                return;
            }
        }

        Scanner scanner = new Scanner(System.in);

        // 1. Pedir al usuario una palabra por teclado
        System.out.print("Introduce la palabra a buscar (se cambiará a MAYÚSCULAS): ");
        String palabraBuscada = scanner.nextLine().trim();

        if (palabraBuscada.isEmpty()) {
            System.out.println("Error: No has introducido ninguna palabra.");
            return;
        }

        // Mostramos el contenido antes de modificar
        System.out.println("\n--- CONTENIDO ACTUAL DEL FICHERO ---");
        mostrarFichero(archivo);

        int lineasModificadas = 0;

        try (RandomAccessFile raf = new RandomAccessFile(archivo, "rw")) {
            // 2. Recorrer el fichero línea a línea
            while (true) {
                // 3. Guardar la posición en la que empieza cada línea antes de leerla
                long posInicioLinea = raf.getFilePointer();

                String linea = raf.readLine();
                if (linea == null) {
                    break; // Fin del fichero
                }

                // Guardamos dónde empieza la siguiente línea
                long posSiguienteLinea = raf.getFilePointer();

                // 4. Comprobar si la palabra buscada aparece en la línea
                if (linea.contains(palabraBuscada)) {
                    // 5. Si aparece, sustituirla por su versión en mayúsculas
                    String lineaModificada = linea.replace(palabraBuscada, palabraBuscada.toUpperCase());

                    // 6. Volver a la posición donde empezaba la línea
                    raf.seek(posInicioLinea);

                    // 7. Escribir de nuevo la línea completa modificada
                    raf.writeBytes(lineaModificada);

                    // Volvemos a situar el puntero donde comenzaba la siguiente línea
                    raf.seek(posSiguienteLinea);

                    lineasModificadas++;
                }
            }

            if (lineasModificadas > 0) {
                System.out.println("\n¡Palabra modificada en " + lineasModificadas + " línea(s)!");
            } else {
                System.out.println("\nLa palabra '" + palabraBuscada + "' no se ha encontrado en el fichero.");
            }

        } catch (IOException e) {
            System.out.println("Error al trabajar con el fichero: " + e.getMessage());
        }

        // Mostramos el contenido final tras las modificaciones
        System.out.println("\n--- CONTENIDO TRAS LA MODIFICACIÓN ---");
        mostrarFichero(archivo);
    }

    // Método auxiliar para mostrar el archivo por consola
    private static void mostrarFichero(File archivo) {
        try (RandomAccessFile raf = new RandomAccessFile(archivo, "r")) {
            String linea;
            while ((linea = raf.readLine()) != null) {
                System.out.println(linea);
            }
        } catch (IOException e) {
            System.out.println("Error al leer el fichero: " + e.getMessage());
        }
    }
}
