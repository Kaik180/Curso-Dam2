package Ejemplos;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class EjemploFlujosCaracteres {
    public static void main(String[] args) {
        // --- A. Carácter a carácter con FileWriter y FileReader ---
        String str = "Este es un ejemplo de escritura usando FileWriter.";
        try (FileWriter fw = new FileWriter("./output.txt")) {
            fw.write(str);
            fw.flush(); // Fuerza el guardado antes de cerrar
        } catch (IOException e) {
            System.out.println("Error E/S: " + e.getMessage());
        }

        try (FileReader fr = new FileReader("./output.txt")) {
            int ch = fr.read();
            while (ch != -1) { // -1 indica el fin de fichero
                System.out.print((char) ch);
                ch = fr.read();
            }
            System.out.println();
        } catch (IOException e) {
            System.out.println("Error de E/S: " + e.getMessage());
        }

        // --- B. Línea a línea con BufferedWriter y BufferedReader (con try-with-resources) ---
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("./caracteres_Buff.txt"))) {
            writer.write("Hola, mundo con BufferedWriter!");
        } catch (IOException e) {
            e.printStackTrace();
        }

        try (BufferedReader reader = new BufferedReader(new FileReader("./caracteres_Buff.txt"))) {
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
