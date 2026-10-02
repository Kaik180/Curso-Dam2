package procesos;

/**
 * Proceso trabajador independiente para el cálculo de números primos en un rango determinado.
 * <p>
 * Diseñado para ser ejecutado como proceso secundario mediante línea de comandos o {@link ProcessBuilder}.
 * Recibe obligatoriamente dos argumentos:
 * </p>
 * <ul>
 *   <li>{@code args[0]}: Límite inferior del rango (inicio, inclusive).</li>
 *   <li>{@code args[1]}: Límite superior del rango (fin, inclusive).</li>
 * </ul>
 * <p>
 * Si los argumentos son correctos y válidos, calcula la cantidad de primos en el intervalo cerrado [inicio, fin],
 * imprime dicho total por la salida estándar ({@code stdout}) y finaliza con código de salida {@code 0} (éxito).
 * </p>
 * <p>
 * Si los argumentos son incorrectos o los valores del rango son incoherentes, imprime un mensaje descriptivo
 * por la salida de error ({@code stderr}) y finaliza con código de salida {@code 1}.
 * </p>
 *
 * @author Kevin
 * @version 1.0
 */
public final class TrabajadorPrimo {

    /**
     * Constructor privado para evitar la instanciación directa de una clase puramente ejecutable.
     */
    private TrabajadorPrimo() {
        // No instanciable
    }

    /**
     * Evalúa si un número natural dado es primo.
     * <p>
     * Se implementa un algoritmo de división por tentativa optimizado:
     * </p>
     * <ul>
     *   <li>Los números menores o iguales a 1 no son primos.</li>
     *   <li>Los números 2 y 3 son primos.</li>
     *   <li>Se descartan inmediatamente múltiplos de 2 y de 3.</li>
     *   <li>Se prueban únicamente divisores de la forma 6k ± 1 hasta la raíz cuadrada de {@code n}.</li>
     * </ul>
     * <p>
     * Esta optimización reduce drásticamente las operaciones necesarias a complejidad O(sqrt(n)).
     * </p>
     *
     * @param n Número entero positivo a verificar.
     * @return {@code true} si {@code n} es un número primo; {@code false} en caso contrario.
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
     * Cuenta cuántos números primos existen en el intervalo cerrado [inicio, fin].
     *
     * @param inicio Límite inferior del rango (inclusive).
     * @param fin    Límite superior del rango (inclusive).
     * @return Cantidad de números primos encontrados en dicho rango.
     */
    public static long contarPrimosEnRango(long inicio, long fin) {
        long cuenta = 0;
        for (long i = inicio; i <= fin; i++) {
            if (esPrimo(i)) {
                cuenta++;
            }
        }
        return cuenta;
    }

    /**
     * Punto de entrada principal para el proceso trabajador.
     *
     * @param args Argumentos de la línea de comandos: {@code <inicio>} y {@code <fin>}.
     */
    public static void main(String[] args) {
        // Validación del número de argumentos
        if (args == null || args.length != 2) {
            System.err.println("Error [TrabajadorPrimo]: Se requieren exactamente 2 argumentos: <inicio> <fin>");
            System.exit(1);
        }

        long inicio;
        long fin;

        // Validación del formato numérico
        try {
            inicio = Long.parseLong(args[0]);
            fin = Long.parseLong(args[1]);
        } catch (NumberFormatException e) {
            System.err.println("Error [TrabajadorPrimo]: Los argumentos deben ser números enteros válidos.");
            System.exit(1);
            return;
        }

        // Validación de coherencia del rango
        if (inicio < 1 || inicio > fin) {
            System.err.println("Error [TrabajadorPrimo]: Rango inválido [" + inicio + ", " + fin + "]. Se requiere inicio >= 1 e inicio <= fin.");
            System.exit(1);
            return;
        }

        // Conteo de primos
        long totalPrimos = contarPrimosEnRango(inicio, fin);

        // Envío del resultado por stdout para el proceso maestro
        System.out.println(totalPrimos);
        System.exit(0);
    }
}
