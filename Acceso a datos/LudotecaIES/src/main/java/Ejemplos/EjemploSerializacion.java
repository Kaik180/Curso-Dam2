package Ejemplos;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.util.ArrayList;

// Clase que implementa Serializable
class Videojuego implements Serializable {
    private static final long serialVersionUID = 1L;

    private int id;
    private String titulo;
    private double precio;

    public Videojuego(int id, String titulo, double precio) {
        this.id = id;
        this.titulo = titulo;
        this.precio = precio;
    }

    @Override
    public String toString() {
        return id + " - " + titulo + " - " + precio + " €";
    }
}

public class EjemploSerializacion {
    public static void main(String[] args) {
        ArrayList<Videojuego> juegos = new ArrayList<>();
        juegos.add(new Videojuego(1, "Tetris", 19.99));
        juegos.add(new Videojuego(2, "Super Mario Bros", 29.99));

        // 1. Guardar (serializar) la lista completa con una sola llamada a writeObject()
        try (ObjectOutputStream salida = new ObjectOutputStream(
                new FileOutputStream("videojuegos.dat"))) {
            salida.writeObject(juegos);
            System.out.println("Lista de videojuegos guardada");
        } catch (IOException e) {
            System.out.println("Error al guardar: " + e.getMessage());
        }

        // 2. Recuperar (deserializar) la lista completa haciendo casting
        try (ObjectInputStream entrada = new ObjectInputStream(
                new FileInputStream("videojuegos.dat"))) {
            @SuppressWarnings("unchecked")
            ArrayList<Videojuego> recuperados = (ArrayList<Videojuego>) entrada.readObject();

            System.out.println("Videojuegos recuperados del fichero:");
            for (int i = 0; i < recuperados.size(); i++) {
                System.out.println(recuperados.get(i));
            }
        } catch (IOException | ClassNotFoundException e) {
            System.out.println("Error al recuperar: " + e.getMessage());
        }
    }
}
