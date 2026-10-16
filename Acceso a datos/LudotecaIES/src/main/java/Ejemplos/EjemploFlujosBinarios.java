package Ejemplos;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

public class EjemploFlujosBinarios {
    public static void main(String[] args) {
        // --- A. Bytes crudos con FileOutputStream y FileInputStream ---
        try (FileOutputStream fos = new FileOutputStream("./archivo_FOS.dat")) {
            byte[] datos = {65, 66, 67}; // Códigos ASCII de 'A', 'B', 'C'
            fos.write(datos);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }

        try (FileInputStream fis = new FileInputStream("./archivo_FOS.dat")) {
            int byteLeido;
            System.out.print("Bytes leídos como char: ");
            while ((byteLeido = fis.read()) != -1) {
                System.out.print((char) byteLeido);
            }
            System.out.println();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }

        // --- B. Tipos primitivos con DataOutputStream/DataInputStream y Búfer ---
        try (DataOutputStream dos = new DataOutputStream(
                new BufferedOutputStream(new FileOutputStream("./archivo_DOS.dat")))) {
            dos.writeInt(42);
            dos.writeChar('Z');
            dos.writeDouble(99.95);
        } catch (IOException e) {
            System.out.println("IOException: " + e.getMessage());
        }

        // Es obligatorio leer en el mismo orden exacto en que se escribió
        try (DataInputStream dis = new DataInputStream(
                new BufferedInputStream(new FileInputStream("./archivo_DOS.dat")))) {
            int intLeido = dis.readInt();
            char charLeido = dis.readChar();
            double doubleLeido = dis.readDouble();

            System.out.println("intLeido = " + intLeido);
            System.out.println("charLeido = " + charLeido);
            System.out.println("doubleLeido = " + doubleLeido);
        } catch (IOException e) {
            System.out.println("IOException: " + e.getMessage());
        }
    }
}
