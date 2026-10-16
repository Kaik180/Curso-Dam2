package Ejemplos;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class EjemploPathNIO {
    public static void main(String[] args) {
        // --- A. Uso directo con Paths.get() y métodos estáticos de Files ---
        List<String> lista = new ArrayList<>();
        lista.add("Ejemplo de escritura utilizando la clase Path");
        lista.add("Se utilizan métodos estáticos");

        Path p1 = Paths.get("./fichPath.txt");
        try {
            // Escritura directa de una lista
            Files.write(p1, lista);

            // Lectura directa de todas las líneas
            List<String> leidas = Files.readAllLines(p1);
            for (String s : leidas) {
                System.out.println(s);
            }
        } catch (IOException e) {
            System.out.println("No se ha podido operar con el fichero: " + e.getMessage());
        }

        // --- B. Uso de FileSystems con BufferedWriter y BufferedReader ---
        Path p2 = FileSystems.getDefault().getPath("./ficPathFS.txt");
        try (BufferedWriter bw = Files.newBufferedWriter(p2)) {
            bw.write("Hola en fichero con FileSystem");
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        try (BufferedReader br = Files.newBufferedReader(p2)) {
            System.out.println(br.readLine());
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
