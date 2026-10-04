package es.iesmutxamel.ludoteca;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

public class GestionarVideojuegos {

    private static final String RUTA_FICHERO = "src/ficheros/videojuegos.txt";

    // Escribir un videojuego al final del fichero
    public void escribirVideojuegoAlFinal(Videojuego videojuego) {
        File archivo = new File(RUTA_FICHERO);

        if (archivo.getParentFile() != null && !archivo.getParentFile().exists()) {
            archivo.getParentFile().mkdirs();
        }

        // FileWriter con true para escribir al final
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(archivo, true))) {
            bw.write(videojuego.toString());
            bw.newLine();
        } catch (IOException e) {
            System.out.println("Error al escribir al final: " + e.getMessage());
        }
    }

    // Escribir un videojuego al principio del fichero
    public void escribirVideojuegoAlPrincipio(Videojuego videojuego) {
        File archivo = new File(RUTA_FICHERO);

        if (archivo.getParentFile() != null && !archivo.getParentFile().exists()) {
            archivo.getParentFile().mkdirs();
        }

        ArrayList<String> lineas = new ArrayList<>();

        // Leemos primero lo que ya hay en el archivo
        if (archivo.exists()) {
            try (BufferedReader br = new BufferedReader(new FileReader(archivo))) {
                String linea;
                while ((linea = br.readLine()) != null) {
                    lineas.add(linea);
                }
            } catch (IOException e) {
                System.out.println("Error al leer el archivo: " + e.getMessage());
            }
        }

        // Sobrescribimos poniendo el nuevo juego al principio
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(archivo, false))) {
            bw.write(videojuego.toString());
            bw.newLine();

            for (String linea : lineas) {
                bw.write(linea);
                bw.newLine();
            }
        } catch (IOException e) {
            System.out.println("Error al escribir al principio: " + e.getMessage());
        }
    }

    // Mostrar el contenido del fichero por consola
    public void mostrarContenido() {
        File archivo = new File(RUTA_FICHERO);

        if (!archivo.exists() || archivo.length() == 0) {
            System.out.println("El fichero no existe o está vacío.");
            return;
        }

        try (BufferedReader br = new BufferedReader(new FileReader(archivo))) {
            String linea;
            while ((linea = br.readLine()) != null) {
                System.out.println(linea);
            }
        } catch (IOException e) {
            System.out.println("Error al leer el contenido: " + e.getMessage());
        }
    }
}
