package org.example;

public class Raton implements Runnable {
    private String nombre;
    private int tiempoAlimentacion;

    public Raton(String nombre, int tiempoAlimentacion) {
        super();
        this.nombre = nombre;
        this.tiempoAlimentacion = tiempoAlimentacion;
    }

    public void comer() {
        try {
            System.out.printf("El ratón %s ha comenzado a alimentarse\n", nombre);
            Thread.sleep(tiempoAlimentacion * 1000);
            System.out.printf("El ratón %s ha terminado de alimentarse\n", nombre);
        } catch (InterruptedException ie) {
            System.out.println("Error comiendo:" + ie.toString());
        }
    }

    @Override
    public void run() {
        this.comer();
    }

    public String getNombre() {
        return nombre;
    }

    public static void main(String[] args) {
        Raton fievel = new Raton("Fievel", 4);
        Raton jerry = new Raton("Jerry", 5);
        Raton pinky = new Raton("Pinky", 3);
        Raton mickey = new Raton("Mickey", 6);
        Thread[] hilos = new Thread[4];
        int quedan = 4;

        hilos[0] = new Thread(fievel);
        hilos[1] = new Thread(jerry);
        hilos[2] = new Thread(pinky);
        hilos[3] = new Thread(mickey);

        for (int i = 0; i < 4; i++) {
            hilos[i].start();
        }

        while (quedan > 0) {
            quedan = 0;

            for (int i = 0; i < 4; i++) {
                if (hilos[i].isAlive()) {
                    quedan++;
                }
                System.out.println("El estado de " + i + " es " + hilos[i].getState());
            }

            try {
                Thread.sleep(1000);
            } catch (InterruptedException ie) {
                System.out.println("Error esperando hilos:" + ie.toString());
            }

            System.out.println("Esperando " + quedan + " hilos");
        }
        System.out.println("Fin del programa principal");
    }
}
