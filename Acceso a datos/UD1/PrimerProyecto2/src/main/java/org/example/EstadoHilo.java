package org.example;

public class EstadoHilo {
    public static void main(String[] args) {
        HiloAuxiliar hilo1 = new HiloAuxiliar();

        System.out.println("Hilo Auxiliar Nuevo: Estado = " + hilo1.getState());

        hilo1.start();
        System.out.println("Hilo Auxiliar Iniciado: Estado = " + hilo1.getState());

        try {
            System.out.println("Esperamos a que termine el hilo...");
            hilo1.join();
        } catch (InterruptedException e) {
            System.err.println("Hilo interrumpido: " + e.getMessage());
            Thread.currentThread().interrupt();
        }

        System.out.println("\nHilo Auxiliar Muerto: Estado = " + hilo1.getState());
    }
}

class HiloAuxiliar extends Thread {
    @Override
    public void run() {
        for (int i = 10; i >= 1; i--) {
            System.out.print(i + ",");
        }
    }
}

