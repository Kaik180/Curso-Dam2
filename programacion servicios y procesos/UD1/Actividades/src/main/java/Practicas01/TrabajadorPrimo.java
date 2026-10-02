package Practicas01;

/**
 * Proceso trabajador independiente para el cálculo de números primos en un rango determinado.
 * <p>
 * Clase réplica en el paquete Practicas01 para compatibilidad directa con el proyecto.
 * </p>
 *
 * @author Kevin
 * @version 1.0
 */
public class TrabajadorPrimo {

    public static boolean esPrimo(long n) {
        if (n <= 1) return false;
        if (n <= 3) return true;
        if (n % 2 == 0 || n % 3 == 0) return false;
        for (long i = 5; i * i <= n; i += 6) {
            if (n % i == 0 || n % (i + 2) == 0) return false;
        }
        return true;
    }

    public static long contarPrimosEnRango(long inicio, long fin) {
        long cuenta = 0;
        for (long i = inicio; i <= fin; i++) {
            if (esPrimo(i)) cuenta++;
        }
        return cuenta;
    }

    public static void main(String[] args) {
        if (args.length != 2) {
            System.err.println("Error [TrabajadorPrimo]: Se requieren exactamente 2 argumentos: <inicio> <fin>");
            System.exit(1);
        }

        long inicio;
        long fin;

        try {
            inicio = Long.parseLong(args[0]);
            fin = Long.parseLong(args[1]);
        } catch (NumberFormatException e) {
            System.err.println("Error [TrabajadorPrimo]: Los argumentos deben ser números enteros válidos.");
            System.exit(1);
            return;
        }

        if (inicio < 1 || inicio > fin) {
            System.err.println("Error [TrabajadorPrimo]: Rango inválido [" + inicio + ", " + fin + "].");
            System.exit(1);
            return;
        }

        long totalPrimos = contarPrimosEnRango(inicio, fin);
        System.out.println(totalPrimos);
        System.exit(0);
    }
}
