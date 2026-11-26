import java.util.Scanner;

class BuscadorPrimos extends Thread {
    private final int inicio;
    private final int fin;
    private int cantidadPrimos;

    public BuscadorPrimos(int inicio, int fin) {
        this.inicio = inicio;
        this.fin = fin;
        this.cantidadPrimos = 0;
    }

    private boolean esPrimo(int numero) {
        if (numero <= 1) {
            return false;
        }
        if (numero == 2) {
            return true;
        }
        if (numero % 2 == 0) {
            return false;
        }
        for (int i = 3; i * i <= numero; i += 2) {
            if (numero % i == 0) {
                return false;
            }
        }
        return true;
    }

    @Override
    public void run() {
        for (int i = inicio; i <= fin; i++) {
            if (esPrimo(i)) {
                cantidadPrimos++;
            }
        }
        System.out.println("Hilo [" + getName() + "] calculó " + cantidadPrimos
                + " primos en el rango [" + inicio + " - " + fin + "]");
    }

    public int getCantidadPrimos() {
        return cantidadPrimos;
    }
}

public class PrimosHilos {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Introduce el número máximo (N): ");
        int n = scanner.nextInt();

        System.out.print("Introduce el número de hilos: ");
        int numHilos = scanner.nextInt();

        BuscadorPrimos[] hilos = new BuscadorPrimos[numHilos];
        int rango = n / numHilos;

        long tiempoInicio = System.currentTimeMillis();

        for (int i = 0; i < numHilos; i++) {
            int inicio = i * rango + 1;
            int fin = (i == numHilos - 1) ? n : (i + 1) * rango;

            hilos[i] = new BuscadorPrimos(inicio, fin);
            hilos[i].start();
        }

        int totalPrimos = 0;
        for (int i = 0; i < numHilos; i++) {
            try {
                hilos[i].join();
                totalPrimos += hilos[i].getCantidadPrimos();
            } catch (InterruptedException e) {
                System.err.println("El hilo fue interrumpido: " + e.getMessage());
            }
        }

        long tiempoFin = System.currentTimeMillis();
        long tiempoTotal = tiempoFin - tiempoInicio;

        System.out.println("\nTotal de primos encontrados: " + totalPrimos);
        System.out.println("Tiempo total: " + tiempoTotal + " ms");

        scanner.close();
    }
}
