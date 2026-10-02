package procesos;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

/**
 * Proceso maestro / coordinador encargado de orquestar el cálculo paralelo de números primos.
 * <p>
 * Implementa la arquitectura multiproceso en Java siguiendo estos pasos:
 * </p>
 * <ol>
 *   <li>Divide el rango completo [1, N] en M subrangos contiguos y equitativos.</li>
 *   <li>Lanza M procesos hijos independientes ejecutando {@link TrabajadorPrimo} mediante {@link ProcessBuilder}.</li>
 *   <li>Recoge la salida estándar generada por cada proceso utilizando {@link BufferedReader}.</li>
 *   <li>Sincroniza la finalización de los subprocesos con {@link Process#waitFor()} y verifica sus códigos de retorno.</li>
 *   <li>Totaliza las sumas parciales de números primos y calcula el tiempo total de procesamiento.</li>
 * </ol>
 *
 * @author Kevin
 * @version 1.0
 */
public final class MaestroProcesos {

    /**
     * Parámetro por defecto para el límite superior del rango de búsqueda.
     */
    public static final long DEFAULT_N = 200_000;

    /**
     * Parámetro por defecto para el número de subprocesos paralelos a instanciar.
     */
    public static final int DEFAULT_M = 4;

    /**
     * Constructor privado para evitar la instanciación de la clase orquestadora.
     */
    private MaestroProcesos() {
        // No instanciable
    }

    /**
     * Obtiene de forma robusta la ruta al ejecutable de Java utilizado por la JVM actual.
     * <p>
     * Esto previene errores de "command not found" en entornos donde Java no se encuentra
     * explícitamente en el PATH del sistema operativo (por ejemplo, entornos IDE).
     * </p>
     *
     * @return Ruta absoluta al binario {@code java} o {@code "java"} como fallback.
     */
    public static String obtenerComandoJava() {
        String javaHome = System.getProperty("java.home");
        if (javaHome != null && !javaHome.isEmpty()) {
            File javaBin = new File(javaHome, "bin/java");
            if (javaBin.exists()) {
                return javaBin.getAbsolutePath();
            }
            File javaExe = new File(javaHome, "bin/java.exe");
            if (javaExe.exists()) {
                return javaExe.getAbsolutePath();
            }
        }
        return "java";
    }

    /**
     * Divide un rango cerrado [1, N] en M subintervalos contiguos lo más homogéneos posible.
     * <p>
     * Si {@code N} no es divisible exactamente entre {@code M}, el residuo ({@code N % M})
     * se distribuye añadiendo una unidad a los primeros subintervalos.
     * </p>
     *
     * @param n           Límite superior total (desde 1 hasta N).
     * @param numProcesos Número de subprocesos / particiones.
     * @return Matriz de dimensiones {@code [M][2]} donde cada fila contiene {@code [inicio, fin]}.
     */
    public static long[][] dividirRangos(long n, int numProcesos) {
        long[][] rangos = new long[numProcesos][2];
        long tamanoBase = n / numProcesos;
        long resto = n % numProcesos;
        long cursor = 1;

        for (int i = 0; i < numProcesos; i++) {
            long tamanoActual = tamanoBase + (i < resto ? 1 : 0);
            long inicio = cursor;
            long fin = cursor + tamanoActual - 1;

            rangos[i][0] = inicio;
            rangos[i][1] = fin;

            cursor = fin + 1;
        }

        return rangos;
    }

    /**
     * Ejecuta el cálculo multiproceso para un límite superior y un número de procesos dados.
     *
     * @param n           Límite superior del rango [1, N].
     * @param numProcesos Número de procesos trabajadores a lanzar.
     * @return Objeto con los resultados agregados (total de primos y tiempo empleado).
     */
    public static ResultadoMultiproceso ejecutar(long n, int numProcesos) {
        System.out.println("==============================================================");
        System.out.println("   CALCULO PARALELO DE PRIMOS (MULTIPROCESO EN JAVA)         ");
        System.out.println("==============================================================");
        System.out.printf("Rango total: [1, %,d]%n", n);
        System.out.printf("Numero de procesos (M): %d%n", numProcesos);
        System.out.println("--------------------------------------------------------------");

        long[][] rangos = dividirRangos(n, numProcesos);
        String javaCmd = obtenerComandoJava();
        String classpath = System.getProperty("java.class.path");
        if (classpath == null || classpath.isEmpty()) {
            classpath = ".";
        }

        List<Process> listaProcesos = new ArrayList<>(numProcesos);

        long tiempoInicio = System.currentTimeMillis();

        // 1. Lanzamiento no bloqueante de todos los subprocesos en paralelo
        for (int i = 0; i < numProcesos; i++) {
            long subInicio = rangos[i][0];
            long subFin = rangos[i][1];

            List<String> comando = new ArrayList<>();
            comando.add(javaCmd);
            comando.add("-cp");
            comando.add(classpath);
            comando.add(TrabajadorPrimo.class.getName());
            comando.add(String.valueOf(subInicio));
            comando.add(String.valueOf(subFin));

            ProcessBuilder pb = new ProcessBuilder(comando);
            try {
                Process proceso = pb.start();
                listaProcesos.add(proceso);
            } catch (IOException e) {
                System.err.printf("Error al lanzar el subproceso %d: %s%n", (i + 1), e.getMessage());
                listaProcesos.add(null);
            }
        }

        // 2. Recolección de salidas y sincronización con waitFor()
        long totalPrimos = 0;
        boolean errorPresente = false;

        System.out.println("Seguimiento y recoleccion de los subprocesos:");
        for (int i = 0; i < numProcesos; i++) {
            Process p = listaProcesos.get(i);
            long subInicio = rangos[i][0];
            long subFin = rangos[i][1];

            if (p == null) {
                System.err.printf("  [Proceso %d] No pudo ser iniciado.%n", (i + 1));
                errorPresente = true;
                continue;
            }

            String lineaSalida = null;
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()))) {
                lineaSalida = reader.readLine();
            } catch (IOException e) {
                System.err.printf("  [Proceso %d] Error leyendo stdout: %s%n", (i + 1), e.getMessage());
            }

            try {
                int exitCode = p.waitFor();
                if (exitCode == 0 && lineaSalida != null) {
                    long primosSubrango = Long.parseLong(lineaSalida.trim());
                    totalPrimos += primosSubrango;
                    System.out.printf("  [Proceso %d] Rango [%,10d - %,10d] -> %,8d primos (exit code: %d)%n",
                            (i + 1), subInicio, subFin, primosSubrango, exitCode);
                } else {
                    errorPresente = true;
                    // Leer salida de error para depuración
                    String lineaError = null;
                    try (BufferedReader errReader = new BufferedReader(new InputStreamReader(p.getErrorStream()))) {
                        lineaError = errReader.readLine();
                    } catch (IOException ignored) {}

                    System.err.printf("  [Proceso %d] Finalizo con error (exit code: %d): %s%n",
                            (i + 1), exitCode, (lineaError != null ? lineaError : "Sin mensaje de error"));
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                System.err.printf("  [Proceso %d] Proceso interrumpido inesperadamente.%n", (i + 1));
                errorPresente = true;
            } catch (NumberFormatException e) {
                System.err.printf("  [Proceso %d] Salida no numerica: '%s'%n", (i + 1), lineaSalida);
                errorPresente = true;
            }
        }

        long tiempoFin = System.currentTimeMillis();
        long duracionTotalMs = tiempoFin - tiempoInicio;

        System.out.println("--------------------------------------------------------------");
        if (errorPresente) {
            System.out.println("AVISO: Uno o mas subprocesos reportaron errores.");
        }
        System.out.println("RESULTADOS MULTIPROCESO:");
        System.out.printf("  Total de numeros primos encontrados: %,d%n", totalPrimos);
        System.out.printf("  Tiempo total transcurrido:           %,d ms (%.3f s)%n",
                duracionTotalMs, duracionTotalMs / 1000.0);
        System.out.println("==============================================================\n");

        return new ResultadoMultiproceso(totalPrimos, duracionTotalMs, numProcesos, n);
    }

    /**
     * Estructura inmutable que encapsula las métricas resultantes de la ejecución multiproceso.
     */
    public static class ResultadoMultiproceso {
        /**
         * Cantidad total de números primos calculados agregando todos los subprocesos.
         */
        public final long totalPrimos;

        /**
         * Duración total de la ejecución en milisegundos.
         */
        public final long duracionMs;

        /**
         * Número de procesos paralelos utilizados.
         */
        public final int numProcesos;

        /**
         * Límite superior evaluado.
         */
        public final long n;

        /**
         * Construye una nueva instancia con las métricas de la ejecución.
         *
         * @param totalPrimos Total de primos encontrados.
         * @param duracionMs  Tiempo transcurrido en milisegundos.
         * @param numProcesos Cantidad de procesos empleados.
         * @param n           Límite superior evaluado.
         */
        public ResultadoMultiproceso(long totalPrimos, long duracionMs, int numProcesos, long n) {
            this.totalPrimos = totalPrimos;
            this.duracionMs = duracionMs;
            this.numProcesos = numProcesos;
            this.n = n;
        }
    }

    /**
     * Punto de entrada principal para el proceso maestro.
     *
     * @param args Argumentos opcionales: {@code args[0] = N}, {@code args[1] = M}.
     */
    public static void main(String[] args) {
        long n = DEFAULT_N;
        int numProcesos = DEFAULT_M;

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

        if (args != null && args.length >= 2) {
            try {
                numProcesos = Integer.parseInt(args[1]);
                if (numProcesos < 1) {
                    System.err.println("El numero de procesos M debe ser al menos 1.");
                    return;
                }
            } catch (NumberFormatException e) {
                System.err.println("Parametro M invalido. Se utilizara el valor por defecto: " + DEFAULT_M);
                numProcesos = DEFAULT_M;
            }
        }

        ejecutar(n, numProcesos);
    }
}
