package es.iesmutxamel.ludoteca;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class VideojuegoTest {

    private Videojuego videojuego;

    @BeforeEach
    public void setUp() {
        videojuego = new Videojuego(100, "The Witcher 3", "PC", 29.99, 10);
    }

    @Test
    public void testCrearVideojuegoCorrectamente() {
        assertNotNull(videojuego);
        assertEquals(100, videojuego.getId());
        assertEquals("The Witcher 3", videojuego.getTitulo());
        assertEquals("PC", videojuego.getPlataforma());
        assertEquals(29.99, videojuego.getPrecio(), 0.001);
        assertEquals(10, videojuego.getStock());
    }

    @Test
    public void testModificarAtributosConSetters() {
        videojuego.setId(200);
        videojuego.setTitulo("Cyberpunk 2077");
        videojuego.setPlataforma("PS5");
        videojuego.setPrecio(49.95);
        videojuego.setStock(5);

        assertEquals(200, videojuego.getId());
        assertEquals("Cyberpunk 2077", videojuego.getTitulo());
        assertEquals("PS5", videojuego.getPlataforma());
        assertEquals(49.95, videojuego.getPrecio(), 0.001);
        assertEquals(5, videojuego.getStock());
    }

    @Test
    public void testToStringFormatoCorrecto() {
        String texto = videojuego.toString();
        assertTrue(texto.contains("100"));
        assertTrue(texto.contains("The Witcher 3"));
        assertTrue(texto.contains("PC"));
        assertTrue(texto.contains("29.99"));
        assertTrue(texto.contains("10"));
    }
}
