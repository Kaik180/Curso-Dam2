package Ejemplos;

public class EjemploTipos {
    public static void main(String[] args) {
        // Declaración de tipos primitivos básicos
        int numeroPrimitivo = 100;       // 4 bytes
        double precio = 19.99;           // 8 bytes
        char letra = 'A';                // 2 bytes
        boolean activo = true;           // 1 byte

        // Uso de la clase equivalente Integer para conversión de tipos
        Integer integer = 300;
        String string = integer.toString();

        // Diferencia entre suma aritmética y concatenación de texto
        int suma = integer + 50;         // Resultado: 350
        String concat = string + 50;     // Resultado: "30050"

        System.out.println("integer = " + integer);
        System.out.println("string = " + string);
        System.out.println("suma = " + suma);
        System.out.println("concat = " + concat);
    }
}
