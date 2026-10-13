package tf4;

import java.io.File;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.util.Scanner;

public class ModificarEntero {

    public static void main(String[] args) {
        String nombreFichero = "enteros.dat";
        File archivo = new File(nombreFichero);

        // Si el archivo no existe o está vacío, escribimos unos enteros de prueba
        if (!archivo.exists() || archivo.length() == 0) {
            try (RandomAccessFile rafCrear = new RandomAccessFile(archivo, "rw")) {
                int[] valoresIniciales = {10, 25, 42, 77, 99};
                for (int valor : valoresIniciales) {
                    rafCrear.writeInt(valor);
                }
                System.out.println("Fichero 'enteros.dat' creado con 5 valores de prueba: 10, 25, 42, 77, 99\n");
            } catch (IOException e) {
                System.out.println("Error al inicializar el fichero: " + e.getMessage());
                return;
            }
        }

        Scanner scanner = new Scanner(System.in);

        // 1. Abrir el fichero en modo lectura y escritura ("rw")
        try (RandomAccessFile raf = new RandomAccessFile(archivo, "rw")) {

            // 2. Calcular cuántos enteros contiene el fichero (un int ocupa 4 bytes)
            long tamanoBytes = raf.length();
            int totalEnteros = (int) (tamanoBytes / 4);

            System.out.println("El fichero contiene " + totalEnteros + " enteros.");

            // Mostramos los valores actuales para que el usuario pueda verlos
            System.out.print("Valores actuales en el fichero: [");
            for (int i = 0; i < totalEnteros; i++) {
                raf.seek((long) i * 4);
                System.out.print(raf.readInt() + (i < totalEnteros - 1 ? ", " : ""));
            }
            System.out.println("]\n");

            // 3. Pedir al usuario la posición del entero que desea modificar
            // 4. Comprobar que la posición esté entre 1 y el total de enteros almacenados
            int posicion = 0;
            while (true) {
                System.out.print("Introduce la posición del entero que deseas modificar (1 a " + totalEnteros + "): ");
                if (scanner.hasNextInt()) {
                    posicion = scanner.nextInt();
                    if (posicion >= 1 && posicion <= totalEnteros) {
                        break;
                    } else {
                        System.out.println("Posición no válida. Debe estar entre 1 y " + totalEnteros + ".");
                    }
                } else {
                    System.out.println("Error: Debes introducir un número entero.");
                    scanner.next(); // Limpiar entrada incorrecta
                }
            }

            // 5. Calcular en qué byte comienza ese entero
            // La posición 1 empieza en el byte 0, la 2 en el byte 4, etc.
            long posicionByte = (long) (posicion - 1) * 4;

            // 6. Situar el puntero en esa posición utilizando seek()
            raf.seek(posicionByte);

            // 7. Leer y mostrar el valor actual almacenado en esa posición
            int valorActual = raf.readInt();
            System.out.println("Valor actual en la posición " + posicion + ": " + valorActual);

            // 8. Pedir al usuario el nuevo valor
            System.out.print("Introduce el nuevo valor: ");
            while (!scanner.hasNextInt()) {
                System.out.println("Error: Debes introducir un número entero.");
                scanner.next();
            }
            int nuevoValor = scanner.nextInt();

            // 9. Volver a la posición correspondiente y sobrescribir únicamente ese entero
            raf.seek(posicionByte);
            raf.writeInt(nuevoValor);

            System.out.println("\n¡Entero modificado correctamente!");

            // Mostramos los valores actualizados para comprobar el cambio
            System.out.print("Valores actualizados: [");
            for (int i = 0; i < totalEnteros; i++) {
                raf.seek((long) i * 4);
                System.out.print(raf.readInt() + (i < totalEnteros - 1 ? ", " : ""));
            }
            System.out.println("]");

        } catch (IOException e) {
            System.out.println("Error al trabajar con el fichero: " + e.getMessage());
        }
    }
}
