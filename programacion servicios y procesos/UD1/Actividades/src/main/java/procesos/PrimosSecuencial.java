package procesos;

/**
 * Versión secuencial (monoproceso / unihilo) para el cálculo de números primos.
 * <p>
 * Diseñada para servir de referencia empírica (baseline) con la cual comparar el rendimiento,
 * evaluar la sobrecarga de creación de procesos y verificar la exactitud de los resultados obtenidos
 * mediante la solución multiproceso implementada en {@link MaestroProcesos}.
 * </p>
 *
 * @author Kevin
 * @version 1.0
 */
public final class PrimosSecuencial {

    /**
     * Parámetro por defecto para el límite superior del rango de búsqueda.
     */
    public static final long DEFAULT_N = 200_000;

    /**
     * Constructor privado para evitar la instanciación de la clase secuencial.
     */
    private PrimosSecuencial() {
        // No instanciable
    }

    /**
     * Evalúa si un número natural dado es primo utilizando división por tentativa optimizada (6k ± 1).
     *
     * @param n Número a comprobar.
     * @return {@code true} si es primo; {@code false} en caso contrario.
     */
    public static boolean esPrimo(long n) {
        if (n <= 1) {
            return false;
        }
        if (n <= 3) {
            return true;
        }
        if (n % 2 == 0 || n % 3 == 0) {
            return false;
        }
        for (long i = 5; i * i <= n; i += 6) {
            if (n % i == 0 || n % (i + 2) == 0) {
                return false;
            }
        }
        return true;
    }

    /**
     * Cuenta la cantidad de números primos dentro del rango cerrado [1, n].
     *
     * @param n Límite superior del rango.
     * @return Total de números primos encontrados.
     */
    public static long contarPrimos(long n) {
        long total = 0;
        for (long i = 1; i <= n; i++) {
            if (esPrimo(i)) {
                total++;
            }
        }
        return total;
    }

    /**
     * Ejecuta el cálculo secuencial de primos para un rango [1, N] y mide el tiempo transcurrido.
     *
     * @param n Límite superior del intervalo.
     * @return Objeto con el resultado del cálculo y el tiempo empleado en milisegundos.
     */
    public static ResultadoSecuencial ejecutar(long n) {
        System.out.println("==============================================================");
        System.out.println("   CALCULO SECUENCIAL DE PRIMOS (LINEA BASE / MONOPROCESO)   ");
        System.out.println("==============================================================");
        System.out.printf("Rango evaluado: [1, %,d]%n", n);
        System.out.println("Calculando de forma secuencial sin procesos concurrentes...");

        long tiempoInicio = System.currentTimeMillis();
        long totalPrimos = contarPrimos(n);
        long tiempoFin = System.currentTimeMillis();
        long duracionMs = tiempoFin - tiempoInicio;

        System.out.println("--------------------------------------------------------------");
        System.out.println("RESULTADOS SECUENCIAL:");
        System.out.printf("  Total de numeros primos encontrados: %,d%n", totalPrimos);
        System.out.printf("  Tiempo total transcurrido:           %,d ms (%.3f s)%n",
                duracionMs, duracionMs / 1000.0);
        System.out.println("==============================================================\n");

        return new ResultadoSecuencial(totalPrimos, duracionMs, n);
    }

    /**
     * Estructura inmutable para almacenar los resultados del cálculo secuencial.
     */
    public static class ResultadoSecuencial {
        /**
         * Cantidad total de números primos calculados secuencialmente.
         */
        public final long totalPrimos;

        /**
         * Tiempo transcurrido durante el cálculo en milisegundos.
         */
        public final long duracionMs;

        /**
         * Límite superior del rango evaluado.
         */
        public final long n;

        /**
         * Construye una nueva instancia con las métricas del cálculo secuencial.
         *
         * @param totalPrimos Total de primos encontrados.
         * @param duracionMs  Tiempo transcurrido en milisegundos.
         * @param n           Límite superior evaluado.
         */
        public ResultadoSecuencial(long totalPrimos, long duracionMs, long n) {
            this.totalPrimos = totalPrimos;
            this.duracionMs = duracionMs;
            this.n = n;
        }
    }

    /**
     * Punto de entrada principal para la versión secuencial.
     *
     * @param args Argumento opcional: {@code args[0] = N}.
     */
    public static void main(String[] args) {
        long n = DEFAULT_N;

        if (args != null && args.length >= 1) {
            try {
                n = Long.parseLong(args[0]);
                if (n < 1) {
                    System.err.println("El parametro N debe ser un entero positivo.");
                    return;
                }
            } catch (NumberFormatException e) {
                System.err.println("Parametro N invalido. Se utilizara el valor por defecto: " + DEFAULT_N);
                n = DEFAULT_N;
            }
        }

        ejecutar(n);
    }
}
