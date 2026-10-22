package Ejemplos;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;

// Ejemplo del PDF: Introduccion_Java.pdf (Colecciones, Regex, Interfaces/Lambdas y Excepciones)
public class EjemploColeccionesPOO {

    @FunctionalInterface
    interface Operacion {
        int calcular(int a, int b);
    }

    public static void main(String[] args) {
        // 1. Listas (ArrayList: permite duplicados y mantiene orden)
        ArrayList<String> lista = new ArrayList<>();
        lista.add("Java");
        lista.add("XML");
        lista.add("Java");
        System.out.println("Lista (ArrayList): " + lista);

        // 2. Conjuntos (HashSet: NO permite duplicados)
        HashSet<String> conjunto = new HashSet<>(lista);
        System.out.println("Conjunto sin duplicados (HashSet): " + conjunto);

        // 3. Mapas (HashMap: pares clave -> valor)
        HashMap<Integer, String> mapaLibros = new HashMap<>();
        mapaLibros.put(101, "El principito");
        mapaLibros.put(102, "Don Quijote");
        System.out.println("Libro con clave 101 en HashMap: " + mapaLibros.get(101));

        // 4. Expresiones regulares (Regex)
        String email = "alumno@iesmutxamel.com";
        boolean emailValido = email.matches("^[\\w.-]+@[\\w.-]+\\.[a-zA-Z]{2,}$");
        System.out.println("¿Email '" + email + "' válido?: " + emailValido);

        // 5. Interfaz funcional con expresión Lambda
        Operacion suma = (a, b) -> a + b;
        System.out.println("Resultado lambda suma (10 + 25): " + suma.calcular(10, 25));

        // 6. Control de Excepciones con try-catch-finally
        try {
            int resultado = Integer.parseInt("123a"); // Provoca NumberFormatException
            System.out.println(resultado);
        } catch (NumberFormatException e) {
            System.out.println("Excepción capturada: No es un número válido (" + e.getMessage() + ")");
        } finally {
            System.out.println("Bloque finally ejecutado siempre.");
        }
    }
}
