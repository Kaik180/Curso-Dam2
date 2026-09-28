package es.iesmutxamel.ludoteca;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class CatalogoTest {

    private Catalogo catalogo;

    @BeforeEach
    public void setUp() {
        catalogo = new Catalogo();
    }

    @Test
    public void unCatalogoNuevoEstaVacio() {
        assertEquals(0, catalogo.obtenerCantidad());
        assertTrue(catalogo.obtenerVideojuegos().isEmpty());
    }

    @Test
    public void sePuedeAgregarUnVideojuego() {
        Videojuego v = new Videojuego(1, "The Legend of Zelda", "Switch", 59.99, 10);
        boolean resultado = catalogo.agregarVideojuego(v);
        assertTrue(resultado);
        assertEquals(1, catalogo.obtenerCantidad());
        assertEquals(v, catalogo.buscarPorId(1));
    }

    @Test
    public void noSePuedeRepetirUnIdentificador() {
        Videojuego v1 = new Videojuego(1, "The Legend of Zelda", "Switch", 59.99, 10);
        Videojuego v2 = new Videojuego(1, "Super Mario Odyssey", "Switch", 49.99, 5);
        catalogo.agregarVideojuego(v1);
        boolean resultado = catalogo.agregarVideojuego(v2);
        assertFalse(resultado);
        assertEquals(1, catalogo.obtenerCantidad());
    }
}
