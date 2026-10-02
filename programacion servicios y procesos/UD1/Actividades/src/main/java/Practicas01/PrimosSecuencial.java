package Practicas01;

/**
 * Cálculo secuencial de números primos en el paquete Practicas01.
 *
 * @author Kevin
 * @version 1.0
 */
public class PrimosSecuencial {

    public static final long DEFAULT_N = 200_000;

    public static boolean esPrimo(long n) {
        if (n <= 1) return false;
        if (n <= 3) return true;
        if (n % 2 == 0 || n % 3 == 0) return false;
        for (long i = 5; i * i <= n; i += 6) {
            if (n % i == 0 || n % (i + 2) == 0) return false;
        }
        return true;
    }

    public static long contarPrimos(long n) {
        long total = 0;
        for (long i = 1; i <= n; i++) {
            if (esPrimo(i)) total++;
        }
        return total;
    }

    public static void main(String[] args) {
        long n = DEFAULT_N;
        if (args.length >= 1) {
            try { n = Long.parseLong(args[0]); } catch (NumberFormatException ignored) {}
        }

        System.out.println("==============================================================");
        System.out.println("   CALCULO SECUENCIAL DE PRIMOS - Practicas01                 ");
        System.out.println("==============================================================");
        System.out.printf("Rango evaluado: [1, %,d]%n", n);

        long tInicio = System.currentTimeMillis();
        long totalPrimos = contarPrimos(n);
        long duracionMs = System.currentTimeMillis() - tInicio;

        System.out.println("--------------------------------------------------------------");
        System.out.printf("Total primos encontrados: %,d%n", totalPrimos);
        System.out.printf("Tiempo transcurrido:      %,d ms (%.3f s)%n", duracionMs, duracionMs / 1000.0);
        System.out.println("==============================================================");
    }
}
