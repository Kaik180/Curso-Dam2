package es.iesmutxamel.ludoteca;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

public class GestionarVideojuegos {

    // Ruta del fichero donde guardaremos los videojuegos
    private static final String RUTA_FICHERO = "src/ficheros/videojuegos.txt";

    /**
     * Añade la información de un videojuego al final del fichero videojuegos.txt.
     * Si el fichero no existe, se creará automáticamente.
     */
    public void escribirVideojuegoAlFinal(Videojuego videojuego) {
        File archivo = new File(RUTA_FICHERO);

        // Aseguramos que la carpeta contenedora exista
        if (archivo.getParentFile() != null && !archivo.getParentFile().exists()) {
            archivo.getParentFile().mkdirs();
        }

        // Usamos FileWriter con 'true' para activar el modo añadir (append) al final
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(archivo, true))) {
            bw.write(videojuego.toString());
            bw.newLine(); // Cada videojuego en una línea diferente
        } catch (IOException e) {
            System.out.println("Error al escribir el videojuego al final del fichero: " + e.getMessage());
        }
    }

    /**
     * Añade la información de un videojuego al principio del fichero videojuegos.txt.
     * Lee el contenido previo, coloca el nuevo videojuego al inicio y vuelve a escribir todo.
     */
    public void escribirVideojuegoAlPrincipio(Videojuego videojuego) {
        File archivo = new File(RUTA_FICHERO);

        // Aseguramos que la carpeta contenedora exista
        if (archivo.getParentFile() != null && !archivo.getParentFile().exists()) {
            archivo.getParentFile().mkdirs();
        }

        ArrayList<String> lineasExistentes = new ArrayList<>();

        // 1. Si el fichero ya existe, leemos su contenido actual línea a línea
        if (archivo.exists()) {
            try (BufferedReader br = new BufferedReader(new FileReader(archivo))) {
                String linea;
                while ((linea = br.readLine()) != null) {
                    lineasExistentes.add(linea);
                }
            } catch (IOException e) {
                System.out.println("Error al leer el fichero para insertar al principio: " + e.getMessage());
            }
        }

        // 2. Sobrescribimos el fichero colocando el nuevo videojuego en la primera línea
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(archivo, false))) {
            // Escribimos primero el nuevo videojuego
            bw.write(videojuego.toString());
            bw.newLine();

            // Escribimos a continuación las líneas que ya existían previamente
            for (String linea : lineasExistentes) {
                bw.write(linea);
                bw.newLine();
            }
        } catch (IOException e) {
            System.out.println("Error al escribir el videojuego al principio del fichero: " + e.getMessage());
        }
    }

    /**
     * Lee el fichero videojuegos.txt y muestra su contenido por consola línea a línea.
     * Si el fichero no existe o está vacío, muestra un mensaje informativo.
     */
    public void mostrarContenido() {
        File archivo = new File(RUTA_FICHERO);

        // Comprobamos si el fichero no existe o si su tamaño es 0
        if (!archivo.exists() || archivo.length() == 0) {
            System.out.println("El fichero no existe o está vacío.");
            return;
        }

        // Leemos con BufferedReader para mostrar una línea cada vez
        try (BufferedReader br = new BufferedReader(new FileReader(archivo))) {
            String linea;
            while ((linea = br.readLine()) != null) {
                System.out.println(linea);
            }
        } catch (IOException e) {
            System.out.println("Error al leer el contenido del fichero: " + e.getMessage());
        }
    }
}
