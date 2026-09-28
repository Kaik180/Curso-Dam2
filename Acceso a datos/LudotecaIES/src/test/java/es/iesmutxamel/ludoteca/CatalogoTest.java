package es.iesmutxamel.ludoteca;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;

import static org.junit.jupiter.api.Assertions.*;

public class CatalogoTest {

    private Catalogo catalogo;

    @BeforeEach
    public void setUp() {
        catalogo = new Catalogo();
    }

    // --- Tests obligatorios según especificación de la Tarea 3 ---

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

    // --- Tests complementarios de gestión de la colección ---

    @Test
    public void sePuedeBuscarPorId() {
        Videojuego v = new Videojuego(10, "Metroid Prime", "GameCube", 39.99, 4);
        catalogo.agregarVideojuego(v);

        Videojuego encontrado = catalogo.buscarPorId(10);
        assertNotNull(encontrado);
        assertEquals("Metroid Prime", encontrado.getTitulo());

        Videojuego noEncontrado = catalogo.buscarPorId(999);
        assertNull(noEncontrado);
    }

    @Test
    public void sePuedeEliminarPorId() {
        Videojuego v = new Videojuego(20, "Halo", "Xbox", 19.99, 3);
        catalogo.agregarVideojuego(v);
        assertEquals(1, catalogo.obtenerCantidad());

        boolean eliminado = catalogo.eliminarPorId(20);
        assertTrue(eliminado);
        assertEquals(0, catalogo.obtenerCantidad());
        assertNull(catalogo.buscarPorId(20));

        boolean eliminarInexistente = catalogo.eliminarPorId(999);
        assertFalse(eliminarInexistente);
    }

    @Test
    public void calcularTotalUnidadesYValorStock() {
        catalogo.agregarVideojuego(new Videojuego(1, "Juego A", "PC", 10.0, 5));
        catalogo.agregarVideojuego(new Videojuego(2, "Juego B", "PC", 20.0, 3));

        assertEquals(8, catalogo.obtenerTotalUnidades());
        assertEquals(110.0, catalogo.obtenerValorTotalStock(), 0.001);
    }

    @Test
    public void filtrarPorStockMaximo() {
        catalogo.agregarVideojuego(new Videojuego(1, "Juego Poco Stock", "PC", 15.0, 2));
        catalogo.agregarVideojuego(new Videojuego(2, "Juego Mucho Stock", "PC", 30.0, 20));

        ArrayList<Videojuego> pocos = catalogo.buscarPorStockMaximo(3);
        assertEquals(1, pocos.size());
        assertEquals("Juego Poco Stock", pocos.get(0).getTitulo());
    }
}
