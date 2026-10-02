package Practicas01;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

/**
 * Proceso maestro / orquestador en el paquete Practicas01.
 *
 * @author Kevin
 * @version 1.0
 */
public class MaestroProcesos {

    public static final long DEFAULT_N = 200_000;
    public static final int DEFAULT_M = 4;

    public static String obtenerComandoJava() {
        String javaHome = System.getProperty("java.home");
        if (javaHome != null && !javaHome.isEmpty()) {
            File javaBin = new File(javaHome, "bin/java");
            if (javaBin.exists()) return javaBin.getAbsolutePath();
            File javaExe = new File(javaHome, "bin/java.exe");
            if (javaExe.exists()) return javaExe.getAbsolutePath();
        }
        return "java";
    }

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

    public static void main(String[] args) {
        long n = DEFAULT_N;
        int numProcesos = DEFAULT_M;

        if (args.length >= 1) {
            try { n = Long.parseLong(args[0]); } catch (NumberFormatException ignored) {}
        }
        if (args.length >= 2) {
            try { numProcesos = Integer.parseInt(args[1]); } catch (NumberFormatException ignored) {}
        }

        System.out.println("==============================================================");
        System.out.println("   CALCULO PARALELO DE PRIMOS (MULTIPROCESO) - Practicas01    ");
        System.out.println("==============================================================");
        System.out.printf("Rango total: [1, %,d]%n", n);
        System.out.printf("Numero de procesos (M): %d%n", numProcesos);
        System.out.println("--------------------------------------------------------------");

        long[][] rangos = dividirRangos(n, numProcesos);
        String javaCmd = obtenerComandoJava();
        String classpath = System.getProperty("java.class.path");
        if (classpath == null || classpath.isEmpty()) classpath = ".";

        List<Process> listaProcesos = new ArrayList<>(numProcesos);
        long tiempoInicio = System.currentTimeMillis();

        for (int i = 0; i < numProcesos; i++) {
            List<String> comando = new ArrayList<>();
            comando.add(javaCmd);
            comando.add("-cp");
            comando.add(classpath);
            comando.add(TrabajadorPrimo.class.getName());
            comando.add(String.valueOf(rangos[i][0]));
            comando.add(String.valueOf(rangos[i][1]));

            ProcessBuilder pb = new ProcessBuilder(comando);
            try {
                listaProcesos.add(pb.start());
            } catch (IOException e) {
                System.err.printf("Error al lanzar proceso %d: %s%n", (i + 1), e.getMessage());
                listaProcesos.add(null);
            }
        }

        long totalPrimos = 0;
        for (int i = 0; i < numProcesos; i++) {
            Process p = listaProcesos.get(i);
            if (p == null) continue;

            String linea = null;
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()))) {
                linea = reader.readLine();
            } catch (IOException ignored) {}

            try {
                int exitCode = p.waitFor();
                if (exitCode == 0 && linea != null) {
                    long parcial = Long.parseLong(linea.trim());
                    totalPrimos += parcial;
                    System.out.printf("  [Proceso %d] Rango [%,10d - %,10d] -> %,8d primos (exit: %d)%n",
                            (i + 1), rangos[i][0], rangos[i][1], parcial, exitCode);
                } else {
                    System.err.printf("  [Proceso %d] Error con exit code: %d%n", (i + 1), exitCode);
                }
            } catch (Exception e) {
                System.err.printf("  [Proceso %d] Excepción: %s%n", (i + 1), e.getMessage());
            }
        }

        long duracionMs = System.currentTimeMillis() - tiempoInicio;
        System.out.println("--------------------------------------------------------------");
        System.out.printf("Total primos encontrados: %,d%n", totalPrimos);
        System.out.printf("Tiempo transcurrido:      %,d ms (%.3f s)%n", duracionMs, duracionMs / 1000.0);
        System.out.println("==============================================================");
    }
}
