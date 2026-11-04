public class Raton implements Runnable {
    private String nombre;
    private int tiempoAlimentacion;

    public Raton(String nombre, int tiempoAlimentacion) {
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

        // Se asigna el nombre del ratón directamente al Hilo para poder identificarlo después
        hilos[0] = new Thread(fievel, fievel.getNombre());
        hilos[1] = new Thread(jerry, jerry.getNombre());
        hilos[2] = new Thread(pinky, pinky.getNombre());
        hilos[3] = new Thread(mickey, mickey.getNombre());

        for (int i = 0; i < 4; i++) {
            hilos[i].start();
        }

        // Bucle de monitoreo (Polling)
        while (quedan > 0) {
            quedan = 0;

            for (int i = 0; i < 4; i++) {
                if (hilos[i].isAlive()) {
                    quedan++;
                }
                // Ahora usamos hilos[i].getName() para ver el nombre del ratón en lugar de un número
                System.out.println("El estado de " + hilos[i].getName() + " es " + hilos[i].getState());
            }

            try {
                Thread.sleep(1000);
            } catch (InterruptedException ie) {
                System.out.println("Error esperando hilos:" + ie.toString());
            }

            System.out.println("Esperando a " + quedan + " hilos...\n------------------------");
        }

        System.out.println("Fin del programa principal");
    }
}