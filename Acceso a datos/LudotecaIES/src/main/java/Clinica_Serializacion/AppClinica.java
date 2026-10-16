package Clinica_Serializacion;

import java.io.*;
import java.util.ArrayList;

public class AppClinica {
    static void main(String[] args) {
        ArrayList<Mascota>lista = new ArrayList<>();
        lista.add(new Mascota(1,"max","Pastor Aleman", 3));
        lista.add(new Mascota(2,"carmen","Pastor Aleman", 4));
        lista.add(new Mascota(3,"max","Pastor Aleman", 6));


        //Escribir un objeto en un fichero
        try (ObjectOutputStream salida = new ObjectOutputStream(
                new FileOutputStream("mascotas.dat"))) {
            salida.writeObject(lista);
            System.out.println("Mascotas guardado");
        } catch (IOException e) {
            System.out.println("Error al guardar: " + e.getMessage());
        }


        try (ObjectInputStream entrada = new ObjectInputStream(
                new FileInputStream("mascotas.dat"))) {
            ArrayList<Mascota> recuperados =
                    (ArrayList<Mascota>) entrada.readObject();
            for (int i = 0; i < recuperados.size(); i++) {
                System.out.println(recuperados.get(i));
            }
        } catch (IOException | ClassNotFoundException e) {
            System.out.println("Error al recuperar: " + e.getMessage());
        }

    }
}
