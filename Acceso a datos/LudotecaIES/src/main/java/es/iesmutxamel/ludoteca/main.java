package es.iesmutxamel.ludoteca;

public class main {

    static void main() {
        Videojuego The_witcher = new Videojuego(100, "The witcher", "pc", 20.00, 7);
        Videojuego Orbital = new Videojuego(101, "Órbita", "pc", 19.95, 7);
        System.out.println(The_witcher);
        System.out.println(Orbital);
    }
}
