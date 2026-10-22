package Ejemplos;

import java.io.IOException;
import java.io.RandomAccessFile;

// Ejemplo del PDF: UP1_Ficheros_RAF.pdf (Acceso Aleatorio con RandomAccessFile)
public class EjemploRAF {
    // Cada registro tiene: id (int = 4 bytes) + precio (double = 8 bytes) + stock (int = 4 bytes) = 16 bytes
    private static final int TAMANO_REGISTRO = 16;

    public static void main(String[] args) {
        String fichero = "datosVideojuegosRAF.dat";

        // 1. Escribir dos registros de tamaño fijo (16 bytes cada uno)
        try (RandomAccessFile raf = new RandomAccessFile(fichero, "rw")) {
            raf.setLength(0); // Limpiamos el fichero para la prueba

            // Registro 1 (empieza en byte 0)
            raf.writeInt(1);         // 4 bytes (0..3)
            raf.writeDouble(19.99);  // 8 bytes (4..11)
            raf.writeInt(10);        // 4 bytes (12..15)

            // Registro 2 (empieza en byte 16)
            raf.writeInt(2);         // 4 bytes (16..19)
            raf.writeDouble(49.99);  // 8 bytes (20..27)
            raf.writeInt(5);         // 4 bytes (28..31)

            System.out.println("Tamaño total del fichero: " + raf.length() + " bytes.");
        } catch (IOException e) {
            System.out.println("Error al escribir RAF: " + e.getMessage());
        }

        // 2. Modificar directamente el stock del 2.º videojuego sin tocar el resto del fichero
        try (RandomAccessFile raf = new RandomAccessFile(fichero, "rw")) {
            int numeroRegistro = 2;
            long inicioRegistro = (numeroRegistro - 1) * TAMANO_REGISTRO; // (2 - 1) * 16 = byte 16
            long posicionStock = inicioRegistro + 12;                     // 16 + 12 = byte 28

            raf.seek(posicionStock);
            int stockActual = raf.readInt();
            System.out.println("Stock antes de modificar (Registro 2): " + stockActual);

            // Volvemos a colocar el puntero en el byte 28 y sobrescribimos solo ese int
            raf.seek(posicionStock);
            raf.writeInt(99);

            // Comprobamos el nuevo valor leyendo desde el inicio del registro 2
            raf.seek(inicioRegistro);
            int id = raf.readInt();
            double precio = raf.readDouble();
            int nuevoStock = raf.readInt();
            System.out.println("Registro 2 actualizado -> ID: " + id + " | Precio: " + precio + " | Nuevo Stock: " + nuevoStock);
        } catch (IOException e) {
            System.out.println("Error al modificar RAF: " + e.getMessage());
        }
    }
}
